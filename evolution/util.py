from model import Model
from mutate import mutate
from driver.driver import Driver
from driver.main import main
from xml.dom import minidom
from operator import itemgetter
from shutil import copyfile
import numpy as np
import tensorflow as tf
import os
import threading
import subprocess
import csv

def create_initial_model():
    model = Model()
    model.train_multiple([
        'data/drivelog-2017-11-30-23-56-14.csv',
        'data/drivelog-2017-11-30-23-57-12.csv',
        'data/drivelog-2017-11-30-23-58-30.csv',
        'data/drivelog-2017-11-30-23-58-55.csv',
        'data/drivelog-2017-11-30-23-59-27.csv',
        'data/drivelog-2017-12-01-00-00-00.csv',
        'data/testdrive.csv'])
    model.save('models/init')

def create_initial_generation():
    parent_model = 'models/init'
    folder = 'models/gen0/'
    if not os.path.exists(folder):
        os.makedirs(folder)

    model = tf.keras.models.load_model(parent_model)
    tf.keras.models.save_model(model, folder + 'init')

    mean = 0
    std = 0.03
    print("Starting generation of generation 0")
    threads = []
    for i in range(49):
        model_name = "g0m" + str(i)
        threads.append(threading.Thread(target=mutate, args=(parent_model, folder + model_name, mean, std)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Finished generation of generation 0")

def create_next_generation(parent_generation):
    parent_folder = 'models/gen' + str(parent_generation) + '/'
    child_folder = 'models/gen' + str(parent_generation+1) + '/'
    if not os.path.exists(child_folder):
        os.makedirs(child_folder)

    # Get list of results from previous generation and sort
    results_file = open(parent_folder+'results', 'rt')
    results = list(csv.reader(results_file, delimiter=",", quoting=csv.QUOTE_NONE))
    del results[0]
    for i, result in enumerate(results):
        if float(result[1]) < 40.0:
            results[i][1] = str(9999.9)
    results = sorted(results, key=itemgetter(1))
    results = [result[0] for result in results]

    probabilities = []
    # Create array of probabilities for each ranking position
    for i in range(len(results)):
        probabilities.append(1/(i+1))
    # Normalize probabilities
    total_p = sum(probabilities)
    for i,p in enumerate(probabilities):
        probabilities[i] = p/total_p

    print("Starting generation of generation " + str(parent_generation+1))
    # Pick parents which should be kept alive for the next generation
    parents_to_keep = np.random.choice(results,15,p=probabilities,replace=False)
    for parent in parents_to_keep:
        copyfile(parent_folder + parent, child_folder + parent)

    mean = 0
    std = 0.03
    # Pick parents which get a child through mutation
    parents_to_mutate = np.random.choice(results,35,p=probabilities,replace=True)
    threads = []
    for i in range(len(parents_to_mutate)):
        model_name = "g" + str(parent_generation+1) + "m" + str(i)
        threads.append(threading.Thread(target=mutate, args=(parent_folder + parents_to_mutate[i], child_folder + model_name, mean, std)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Finished generation of generation " + str(parent_generation+1))

def drive_model(path):
    model = tf.keras.models.load_model(path)
    driver = Driver(model)
    main(driver)

def grade_model(path):
    config_path = os.path.abspath(".") + "/evo_race.xml"
    torcs = subprocess.Popen(['torcs', '-r', config_path])
    driver = subprocess.Popen(['/home/jarno/miniconda3/envs/torcs/bin/python', '-c', 'import util; util.drive_model(\'' + path + '\')'])
    torcs.wait()
    driver.kill()

    return get_last_result()

def get_last_result():
    # Locate xml file with results and parse
    results_folder = os.environ['HOME'] + "/.torcs/results/evo_race"
    result_files = os.listdir(results_folder)
    result_files.sort()
    last_file = result_files[-1]
    xml = minidom.parse(results_folder + '/' + last_file)

    # Default return values
    time = 9999.9
    top_speed = 0.0
    damage = 9999.9

    # Extract relevant results
    sections = xml.getElementsByTagName("section")
    rank = [s for s in sections if s.getAttribute('name') == "Rank"][0]
    drivers = rank.getElementsByTagName("section")
    for driver in drivers:
        attstrs = driver.getElementsByTagName("attstr")
        name_element = [a for a in attstrs if a.getAttribute('name') == "name"][0]
        if name_element.getAttribute('val') == "scr_server 1":
            attnums = driver.getElementsByTagName("attnum")
            for attnum in attnums:
                name = attnum.getAttribute('name')
                if name == "time":
                    time = attnum.getAttribute('val')
                elif name == "top speed":
                    top_speed = attnum.getAttribute('val')
                elif name == "dammages":
                    damage = attnum.getAttribute('val')

    return time, top_speed, damage

def test_generation(generation, use_old_results):
    path = "models/gen" + str(generation) + "/"

    # Create dictionary of results of previous generation so they do not need to be simulated again
    previous_results_dict = {}
    if generation > 0 and use_old_results:
        previous_results_file = open("models/gen" + str(generation-1) + "/results", 'rt')
        previous_results = list(csv.reader(previous_results_file, delimiter=",", quoting=csv.QUOTE_NONE))
        for result in previous_results[1:]:
            previous_results_dict[result[0]] = result

    files = os.listdir(path)
    files.sort()
    with open(path+"results", 'w') as results:
        results.write("Model,Time,Top speed,Damage\n")

        for file in files:
            # First check if the model comes from the previous generation and if so, copy results
            if file in previous_results_dict:
                print("Gettin+g results for model", file, "from previous generation")
                results.write(",".join(previous_results_dict[file])+"\n")
            # Otherwise test model
            elif file != 'results':
                model_path = path + file
                print("Start testing model", file)
                time, top_speed, damage = grade_model(model_path)
                results.write(",".join([file,time,top_speed,damage])+"\n")
                print("Finished testing model", file, time, top_speed, damage)

if __name__ == '__main__':
    create_initial_generation()
    i = 0
    while(True):
        use_old_results = i%4 != 0 # Retest all models every 4 generations, to prevent a lucky instance
        test_generation(i, use_old_results)
        create_next_generation(i)
        i += 1