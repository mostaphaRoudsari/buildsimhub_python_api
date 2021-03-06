[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.txt)
[![Twitter Follow](https://img.shields.io/twitter/follow/sendgrid.svg?style=social&label=Follow)](https://twitter.com/buildsimhub)

**This library allows you to quickly and easily use the BuildSimHub Web API v1 via Python.**

This library represents the beginning of the Cloud Simulation function on BuildSimHub. We want this library to be community driven and BuildSimHub led. We need your help to realize this goal. To help, make sure we are building the right things in the right order, we ask that you create [issues](https://github.com/weilix88/buildsimhub_python_api/issues) and [pull requests](https://github.com/weilix88/buildsimhub_python_api/pulls) or simply upvote or comment on existing issues or pull requests.
We appreciate your continued support, thank you!

# Table of Contents
* [Latest Update](#update)
* [Installation](#installation)
* [Quick Start](#quick-start)
  * [SimulationJob](#simulation_job)
  * [Model](#energy_model)
  * [Parametric](#parametric_job)
  * [HTML Parser](#eplus_html_parser)
  * [Post-processing Package](#post_process)
   * [Plots](#plots)
* [Objects and Functions](#functions)
* [Standard EEMs library](#eems)
* [Roadmap](#roadmap)
* [About](#about)
* [License](#license)

<a name="update"></a>
The latest version is 1.3.0. Changes include:
1. Fully support EnergyPlus 8.9 cloud simulation
2. Fully support epJSON file upload & simulation
3. add `eio` and `rdd` to extract .eio and .rdd result files
4. Use the developed httpurllib to take out the requests dependency
5. Address compatibility issues with Python 2.7
6. Run method in a SimulationJob supports batch model uploading with one epw file.

<a name="installation"></a>

# Installation

## Prerequisites
- The BuildSimHub service, starting at the [free level](https://my.buildsim.io/register.html)
- Python version 3.4, 3.5 or 3.6, Python 2.7 is undere-testing.

## Install Package
Simply clone / download this repository and place in any folder you wish to build your application on. Examples:
![picture alt](https://imgur.com/x60rk2O.png)

## Setup environment
After you downloaded the whole package, the first you need to do is to reconfigure your user API in the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config) file.
You can find the API key associate with your account under the profile page:

![picture alt](https://imgur.com/gHehDiN.png)

Simply add the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config)
`user_api_key:[YOUR_API_KEY]`
and the `base_url` should be: https://my.buildsim.io/
You can leave the `vendor_id=BuildSimHub` as it is. A sample of a complete info.config file is:
`user_api_key=00268f8c-e538-41bc-8927-a2ba96a639b3
base_url=https://my.buildsim.io/
vendor_id=BuildSimHub`

## Dependencies
- There is no dependecy requirements for using API calls.
- However, if you'd like to utilize our plotly integration function, [plotly python](https://plot.ly/python/getting-started/) is required along with numpy, pandas.

## Project / Model key (optional)
If you want to do simulations under an exisiting project, you will need to retrieve the project or model keys to do it. 
Differences between a project key and a model key:
1. project_key can be found under a project. If this key is supplied, then the API will create a new model under the project.
2. model_key can be found under every model. If a model key is supplied, then the API will create a new model history under the model.
You will then find the model key under the energy model tab (highlighted in the figure below)
![picture alt](https://imgur.com/gO4elTT.png)

<a name="quick-start"></a>

# Quick Start
### Hello BuildSim
```python
from BuildSimHubAPI import buildsimhub
###############NOW, START THE CODE########################

bsh = buildsimhub.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job()
new_sj.run("/Users/weilixu/Desktop/5ZoneAirCooled.idf"
          ,"/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"
          , track=True)
```

The `BuildSimHubAPIClient` creates a [portal object](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py) that manages simulation workflow.
From this object, you can initiate a [simulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) to conduct a cloud simulation. Call `run()` method with parameters can start the cloud simulation.

## Retrieve Cloud simulation results
```python
from BuildSimHubAPI import buildsimhub
bsh = buildsimhub.BuildSimHubAPIClient()

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"

new_sj = bsh.new_simulation_job()
new_sj.run(file_dir, wea_dir, track=True)

######BELOW ARE THE CODE TO RETRIEVE SIMULATION RESULTS#########
response = new_sj.get_simulation_results('html')
print(response)
```
If the simulation job is completed, you can get results by calling `get_simulation_results(type)` function. The function will immediately return the requested results in text format.

<a name="functions"></a>
#Object and Functions

<a name="simulation_job"></a>
## SimulationJob
The easiest way to generate a [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) class is calling the `new_simulation_job()` method in the [BuildSimHubAPIClient](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py).

Optionally, you can provide a `model_key` to create a new [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) instance. The `model_key` can be found under each folder of your project
![picture alt](https://imgur.com/jNrghIZ.png)

Once you provide a `model_key` to instantiate the simulation job, then this job will link to the project, which contains the `model_key`.
Lastly, a simulation job manages one type of cloud simulation. It contains six main functions for cloud simulations.

### run
The `run()` function allows you to upload an energy model and weather file to the platform for cloud simulation (project creation is not required for this method). It has in total 2 parameters.
1. `file_dir` (required): the absolute local directory of your EnergyPlus / OpenStudio model (e.g., "/Users/weilixu/Desktop/5ZoneAirCooled.idf")
2. `epw_dir`(required): the absolute local director of the simulation epw weather file (it should be .epw file)
3. `unit` (optional): provide either `'ip'` or `'si'` unit system for your simulation job.
4. `agent` (optional): The agent number should be selected among 1, 2 or 4 agents. The more agents use for one simulation job, the faster this one simulation job can be finished. The default agent number is 1.

### create_run_model
The `create_run_model()` function allows you to upload an energy model to the platform and run simulaiton. It has in total 4 parameters.
1. `file_dir` (required): the absolute local directory of your EnergyPlus / OpenStudio model (e.g., "/Users/weilixu/Desktop/5ZoneAirCooled.idf")
2. `unit` (optional)
3. `agent` (optional)
4. `comment`(optional): The description of the model version that will be uploaded to your folder. The default message is `Upload through Python API`

### get_simulation_results
The `get_simulation_results(type)` function requires 1 parameter, the result type. Currently, you can retrieve three types of results: the error file (`err`), eso file (`eso`), html file (`html`), eio file(`eio`) and rdd file(`rdd`), generated from EnergyPlus simulation. This method will return the results in text, which you can directly write out into a file.
```python
response = newSimulationJob.get_simulation_results('err')
print (response)
```
### Misc. methods and variables:
Besides the above functions, you can also retrieve some properties of the simulation job:
1. *track_token*: get the tracking token used for connecting the cloud simulation.
2. *model_key*: get the model key which connects to a branch of models

<a name="energy_model"></a>
## Model
The model class contains a set of methods that provides the model information and results (after simulation). It can be generated from the `BuildSimHubAPIClient` with your specific simulation job. Here is an example to generate a model.

```python
bsh = buildsimhub.BuildSimHubAPIClient()
newSj = bsh.new_simulation_job(model_key)
model = bsh.get_model(newSj)
```

### Pre-simulation methods
1. *num_total_floor()*: can be called before simulation is completed. It returns the number of floors, or -1 if there is an error.
2. *num_zones()*: can be called before simulation is completed. It returns the total number of thermal zones, or -1 if there is an error.
3. *num_condition_zones()*: can be called before simulation is completed. It returns the total number of conditioned zones, or -1 if there is an error.
4. *conditioned_floor_area (unit)*: can be called before simulation is completed. It returns the floor areas of conditioned spaces, or -1 if there is an error. This method has an optional input: unit. If you wish to get ft2 unit, then you need to specify 'ip' for the unit parameter:
`  m.condition_floor_area("ip")
`
5. *gross_floor_area(unit)*: can be called before simulation is completed. It returns the total floor areas (including plenum spaces), or -1 if there is an error. This method has an optional input: unit. If you wish to get ft2 unit, then you need to specify 'ip' for the unit parameter:
`  m.gross_floor_area("ip")
`
6. *window_wall_ratio()*: can be called before simulation is completed. It returns the total window to wall ratio (above floor surface area) or -1 if there is an error.
7. *bldg_orientation()*: can be called before simulation is completed. It returns the orientation of the building.
8. *bldg_geo()*: open the browser to view the model 3D geometry

### Post-simulation methods
1. *new_site_eui()*: It returns the net site eui of the simulation (includes generators such as PV). The unit should be based on model specification: SI (kWh/m2 or MJ/m2), IP(kWh/m2).
2. *total_site_eui()*: It returns the total site eui of the simulation. The unit should be based on model specification: SI (kWh/m2 or MJ/m2), IP(kWh/m2).
3. *not_met_hour_cooling()*: returns the time sepoint not met hours during cooling condition period. unit: hour
4. *not_met_hour_heating()*: returns the time sepoint not met hours during heating condition period. unit: hour
5. *not_met_hour_total()*: returns the time sepoint not met hours during heating and cooling condition period. unit: hour
6. *total_end_use_electricity()*: returns the total electricity consumption of the design. unit: kWh or GJ, IP is kBtu
7. *total_end_use_naturalgas()*: returns the total natural gas consumption of the design. unit: kWh or GJ, IP is kBtu
8. *cooling_electricity()*: returns the total electricity consumption of cooling energy. unit: kWh or GJ, Ip is kBtu
9. *domestic_hotwater_electricity()*: returns the total electricity consumption of the service water system. unit: kWh or GJ, IP is kBtu
10. *domestic_hotwater_naturalgas()*: returns the total natural gas consumption of the service water system. unit: kWh or GJ, IP is kBtu
11. *exterior_equipment_electricity()*: returns the total electricity consumption of the exterior equipment. unit: kWh or GJ, IP is kBtu
12. *exterior_equipment_naturalgas()*: returns the total natural gas consumption of the exteiror equipment. unit: kWh or GJ, IP is kBtu
13. *exterior_lighting_electricity()*: returns the total electricity consumption of the exterior lighting system. unit: kWh or GJ, IP is kBtu
14. *exterior_lighting_naturalgas()*: returns the total natural gas consumption of the exterior lighting system. unit: kWh or GJ, IP is kBtu
15. *fan_electricity()*: returns the total electricity consumption of the fan system. unit: kWh or GJ, IP is kBtu
16. *heating_electricity()*: returns the total electricity consumption of the heating system. unit: kWh or GJ, IP is kBtu
17. *heating_naturalgas()*: returns the total natural gas consumption of the heating system. unit: kWh or GJ, IP is kBtu
18. *heat_rejection_electricity()*: returns the electricity consumption of the heat rejection. unit: kWh or GJ, IP is kBtu
19. *heat_rejection_naturalgas()*: returns the natural gas consumption of the heat rejection. unit: kWh or GJ, IP is kBtu
20. *interior_equipment_electricity()*: returns the electricity consumption of the interior equipment. unit: kWh or GJ, IP is kBtu
21. *interior_equipment_naturalgas()*: returns the natural gas consumption of the interior equipment. unit: kWh or GJ, IP is kBtu
22. *interior_lighting_electricity()*: returns the electricity consumption of the interior lighting. unit: kWh or GJ, IP is kBtu
23. *interior_lighting_naturalgas()*: returns the natural gas consumption of the interior lighting. unit: kWh or GJ, IP is kBtu
24. *pumps_electricity()*: returns the electricity consumption of the pumps. unit: kWh or GJ, IP is kBtu
25. *pumps_naturalgas()*: returns the natural gas consumption of the pumps. unit: kWh or GJ, IP is kBtu
26. *zone_load(zone_name)*: This method has two modes. 1. extract list of zones and their total heating / cooling load information. 2. extract one zone's detail load components information. The second mode can be activate by including the `zone_name` variable.
For the first mode, below is the example code and output:
```python
model_result = bsh.get_model(new_sj)
load_profile = model_result.zone_load()

#Output:
#[{'zone_name': 'SPACE1-1', 'heating_unit': 'W', 'cooling_unit': 'W', 'heating_load': -7804.11, 'cooling_load': 7461.61, #'heating_load_density': -78.70219846712384, 'cooling_load_density': 75.2481847519161, 'heating_load_density_unit': 'W/m2', #'cooling_load_density_unit': 'W/m2', 'cooling_peak_load_time': '7/21 15:45:00', 'heating_peak_load_time': '1/21 24:00:00'}, {'zone_name': #'SPACE5-1', 'heating_unit': 'W', 'cooling_unit': 'W', 'heating_load': -6165.32, 'cooling_load': 8356.869999999999, #'heating_load_density': -33.78442654392021, 'cooling_load_density': 45.793577730286586, 'heating_load_density_unit': 'W/m2', #'cooling_load_density_unit': 'W/m2', 'cooling_peak_load_time': '7/21 15:00:00', 'heating_peak_load_time': '1/21 24:00:00'}]
```

### Misc. methods and variables
1. last_parameter_unit: You can check the value of the variable requested by the most recent API call.
```python
m = new_sj.model
print(str(m.net_site_eui())+ " " + m.lastParameterUnit)
#Output: 242.98 MJ/m2
print(str(m.total_end_use_electricity())+ " " + m.lastParameterUnit)
#Output: 156.67 GJ
```
<a name = "parametric_job"></a>
## Parametric Job
Similar to simulation job, the parametric job is another type of cloud simulation. The difference is this class handles batch processings by applying energy efficiency measures from our standard EEMs library. The easiest way to initiate a parametric job is calling the `new_parametric_job()` method in the [BuildSimHubAPIClient](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py).
The method requires user to provide a `model_key`. The `model_key` ties to a model on the platform which we call it as the seed model. Below is the sample code for demonstration purpose.
```python
model_key = 'ec76b257-5dc2-470a-846e-b8897530d'

bsh = bshapi.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(model_key)

# apply EEMs
# window U value
wp = bshapi.measures.WindowUValue()
uValue = [2.0, 1.6, 1.4]
wp.set_datalist(uValue)

# window SHGC
wshgc = bshapi.measures.WindowSHGC()
shgc = [0.5, 0.4, 0.3]
wshgc.set_datalist(shgc)

# wwr
wrr = bshapi.measures.WindowWallRatio()
win = [0.2, 0.3]
wrr.set_datalist(win)

# add these EEM to parametric study
new_pj.add_model_measures(wp)
new_pj.add_model_measures(wshgc)
new_pj.add_model_action(wwr)

# estimate runs and submit job
# print(newPj.num_total_combination())
new_pj.submit_parametric_study(track=True)
```
The full list of EEMs currently available through python API is listed in [EEM library](#(#eems).

### submit_parametric_study()
This is the key method to start a parametric simulations.

<a name = "eplus_html_parser"></a>
## eplusHTMLParser
The eplusHTMLParser provides a set of methods to help users finding data in the EnergyPlus HTML output file. To use this HTML parser, user has to retrieve the processed HTML file from BuildSimHub service. An example code is illustrated below.
```python
from BuildSimHubAPI import eplusHTMLParser
...
  response = new_sj.get_simulation_results('html')
  value_dict = eplusHTMLParser.extract_a_value_from_table(response, 'Annual Building Utility Performance Summary',
    'Site and Source Energy', 'Energy Per Total Building Area', 'Net Site Energy')
  print(value_dict['value] + " " + value_dict['unit'])
  
  #Output: 241.7 MJ/m2
```
### extract_a_value_from_table(report, table, column_name, row_name, reportFor)
This method allows users to extract a specifc cell value from HTML file. It has four required parameters and one optional parameter.
1. `report`: the name of the report in the HTML file. You can find the list of available reports under the Table of Content section in the HTML file.
![picture alt](https://imgur.com/QEB5XXF.png)
2. `table`: the name of the table in the HTML file. You can find the table name under each report. Figure below shows an example of the table name:
![picture alt](https://imgur.com/MYRODca.png)
3. `column_name`: the header of a column which the cell is located in. The header may contains unit, but you do not need to include the unit for this parameter.
![picture alt](https://imgur.com/PTcgcC5.png)
4. `row_name`: the name of the row, typically starts at the first column of a table. The row name may contains unit, but you do not need to include the unit for this parameter.
![picture alt](https://imgur.com/UY3CHPR.png)
5. `reportFor`: This is an optional parameter. The default is set to 'Entire Facility'. Usually, all the report is for entire facility. However, there are some cases where the report is generated for a specific zone, e.g., zone load component reports. Below is the example of finding this parameter in the HTML file.
![picture alt](https://imgur.com/ZiCyT68.png)

<a name="post_process"></a>
## post-processing function
The post-processing functions help post-processing the simulation data extracted from Cloud simulation. These include but not limited to performing basic plottings, and organize the data into the popular pandas dataframe for user customized post processing.

<a name="plots"></a>
## ParametricPlot
The parametric plot class helps organizing parametric data into the popular pandas dataframe (pandas, numpy are required), and offer basic plotting functions for retriving simple and quick plots. With this class, you can either request for the pandas dataframe:
```python
##have user key and model key ready here
results = bsh_api.helpers.ParametricModel(usr_key, model_key)
##request for parametric EUI list
result_dict = results.net_site_eui()
result_unit = results.lastParameterUnit
#get plot
plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)
print(plot.pandas_df())

#OUTPUT:
#        CoolingCOP  LPD   WWR  Value
#case1         3.00  0.6  0.25  54.82
#case2         2.86  0.6  0.25  54.98
#case3         2.80  0.6  0.25  55.05
#case4         3.00  0.9  0.25  57.11
#case5         2.86  0.9  0.25  57.28
```
### Plotly
There are two plots available in the current API library.
1. scatter plot: 
`plot.scatter_chart_plotly(title)` This produce a scatter plot. Title of the graph is an optional input
![picture alt](https://imgur.com/RzNuyse.png)

2. Parallel coordinate:
`plot.parallel_coordinate_plotly(investigate)` This produce a parallel coordinate plot. The investigate is optional, which will color code the lines based on this investigated category. Image below shows the example of investigating the LPD variable.
![picture alt](https://imgur.com/XnaDW7O.png)

More charts can be added to the standard API library - submit a [issues](https://github.com/weilix88/buildsimhub_python_api/issues)!

<a name="eems"></a>
# Standard Energy Efficiency Measure library
In the current version, the standard EEMs library is only available for parametric study.
Standard EEMs library allows user to upload any IDF models (early stage, schematic stage, or detail design) and perform simple parametrics. Apply standard EEMs to your idf models can help designers quickly explore different design options on the cloud, and also save huge time for value engineering at later stage. Below lists the EEMs covered in the recent release:

## Standard EEMs
1. WindowWallRatio: This measure can effectively scale down the overall window to wall ratio (WWR) based on user inputs. But it will ignore all the scale up inputs. For example, the uploaded IDF has WWR of 40%. If user input is 30%, then this measure will scale the WWR of the model to 30%. However, if the user input is 50%, the this measure will not do anything to the model.

2. WindowUValue(unit): This measure will change the window U value to specified user inputs. Unit is optional for this measure. The default unit system is `si`, user can initiate the instance as WindowUValue(`ip`), if the inputs are in ip unit. Also, this measure is required to be applied with WindowSHGC together.

3. WindowSHGC: This measure will change the window SHGC value to specified user inputs. It is required to apply this measure together with WindowUValue measure

4. WallRValue(unit): This measure will change the exterior wall R-value construction to user inputs. The unit is optional with `si` as default.

5. RoofRValue(unit): This measure will change the exterior roof R-value construction to user inputs. The unit is optional with `si` as default.

6. LightLPD(unit): This measure will change the lighting power density (basically all the lights objects) to the desired value (using the watts / floor area method). The unit is optional with `si` as default.

7. OccupancySensor: This measure has no inputs required. Once this object is instantiated, the instance will automatically carry two options: has occupancy sensor and no occupancy sensor. The current approach is to deduct the lighting power density by allowed credit according to ASHRAE 90.1 Appendix G table G3.2.

8. DaylightingSensor: This measure has no inputs required. Once this object is instantiated, the instance will automatically carry two options: has daylight sensor and no daylight sensor. The daylight sensor will be installed in perimeter zones that with windows only. The default properties of daylight sensor (e.g. lighting levels, control method) are set according to EnergyPlus example file (5ZoneVAV-WaterStorage.idf) or the example given in the input/output reference document.

9. CoolingCOP: This measure will change the cooling efficiencies of all coils and chillers according to user inputs. The efficiency measure is COP. If the cooling devices in the seed model have higher COP then the user specified, then their COP will remain the same.

10. CoolingCoilCOP: This measure will change the cooling efficiencies of cooling coils only. The efficiency measure is COP. If cooling coils in the seed model have higher COP then the user specified, then their COP will remain the same.

11. CoolingChillerCOP: This measure will change the cooling efficiencies of chillers only. The efficiency measure is COP. If chillers in the seed model have higher COP then the user specified, then their COP will remain the same.

12. HeatingEfficiency: This measure will change the heating efficiencies of coils and boilers. The efficiency measure is either COP or percent. If user specified data is equal or smaller than 1.0, then this measure will only apply to the heating devices that has heating efficiencies such as boilers or coil:heating:fuel. If user specified data is greater than 1, then this measure will apply to the heating devices that use COP as efficiency metric, such as coil:dx:heating:singlespeed. Similarly, if the heating devices in the seed model have higher efficiencies than user specified, then the measure will not be effective.

## New EEMs
1. WWR South/East/West/North: These are a group of measures that can be used individually to change the window wall ratio of facades facing different orientations.

## How to use
```python
import BuildSimHubAPI as bsh_api

#you can get model_key from your project
model_key = '66667-6sd8-4dff-a51d-4a13ddef5f39'
new_pj = bsh.new_parametric_job(model_key)

#1. for wall insulation measure
wr = bsh_api.measures.WallRValue('ip')
#2. create a list and fill in the parametric values for wall insulation
rValue = [20, 25, 30]
#3. assign the list to the measure
wr.set_datalist(rValue)

#add your new measure to the parametric job
new_pj.add_model_measure(wr)
...
```

<a name="roadmap"></a>
# Roadmap
1. We are working on a standard EEMs, which allows user to apply common energy efficiency measures to any IDF models. Open an issue if you did not see any desired EEMs in the standard EEM library!
2. More simulation configurations and output results return will be added in the future!
3. If you are interested in the future direction of this project, please take a look at our open [issues](https://github.com/weilix88/buildsimhub_python_api/issues) and [pull requests](https://github.com/weilix88/buildsimhub_python_api/pulls). We would love to hear your feedback.


<a name="about"></a>
# About

buildsimhub-python is guided and supported by the BuildSimHub [Developer Experience Team](mailto:haopeng.wang@buildsimhub.net).

buildsimhub-python is maintained and funded by the BuildSimHub, Inc. The names and logos for buildsimhub-python are trademarks of BuildSimHub, Inc.

<a name="license"></a>
# License
[The MIT License (MIT)](LICENSE.txt)

