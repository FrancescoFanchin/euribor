import yaml
import os
import shutil
import fileinput

config_filepath = "dag-config/"
dag_template_filename = "dag-template.py"

for filename in os.listdir(config_filepath):
    with open(config_filepath + filename) as f:
        config = yaml.safe_load(f)
        year_list = list(range(int(config["StartPeriod"]), int(config["EndPeriod"])))
        new_filename = "../dags/" + config["DagId"] + ".py"
        shutil.copyfile(dag_template_filename, new_filename)

        with fileinput.input(new_filename, inplace=True) as file:
            for line in file:
                new_line = (
                    line.replace("dag_id", "'" + config["DagId"] + "'")
                    .replace("scheduletoreplace", config["Schedule"])
                    .replace("querytoreplace", config["Query"])
                    .replace("serieskeytoreplace", config["SeriesKey"])
                    .replace("starttoreplace", str(config["StartPeriod"]))
                    .replace("endtoreplace", str(config["EndPeriod"]))
                    .replace("formattoreplace", config["FileType"])
                    .replace("'email': None", "'email': " + f"'{config['Email']}'")
                )
            

                print(new_line, end="")
