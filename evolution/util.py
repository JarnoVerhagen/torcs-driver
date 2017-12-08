from model import Model
from mutate import mutate
from driver.driver import Driver
from driver.main import main
from xml.dom import minidom
import tensorflow as tf
import os
import threading

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
    std = 0.01
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

def drive_model(path):
    model = tf.keras.models.load_model(path)
    features = 14
    driver = Driver(model, features)
    main(driver)

def grade_model(path):
    config_path = os.path.abspath(".") + "/evo_race.xml"
    os.system(" ".join(['torcs', '-r', config_path, '&'])) # The '&' puts it in the background
    drive_model(path)

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

def test_generation(generation):
    path = "models/gen" + str(generation) + "/"
    files = os.listdir(path)
    results = open(path+"results", 'w')
    results.write("Model,Time,Top speed,Damage\n")

    for file in files:
        if file != 'results':
            model_path = path + file
            print("Start testing model", file)
            time, top_speed, damage = grade_model(model_path)
            results.write(",".join([file,time,top_speed,damage])+"\n")

test_generation(0)