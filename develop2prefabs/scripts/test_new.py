import pathlib
import json
import os
import uuid
import re
from math import sqrt
from uuid import UUID
from subprocess import Popen, PIPE
import subprocess

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    res = (str(uuid_obj) == str(uuid_to_test).lower())
    return res

def updateResourcePack(projectDir, timelineUuid):
    print ("Start updateResourcePack = " + str(timelineUuid))
    filename = os.path.join(projectDir, 'resource-pack.json')

    with open(filename,'r+') as file:
        json_data = json.load(file)
        file.close()
    if 'timelines' not in json_data:
        print ("updateResourcePack json_data = " + str(json_data))
        initMap = []
        dataMap = {
           "@class": "StdResourceMapTimelineResource",
           "map": initMap
        }
        json_data["timelines"] = dataMap
        with open(filename,'w+') as file:
            json.dump(json_data, file, indent = 2)

    with open(filename,'r+') as file:
        json_data = json.load(file)
        file.close()

    map = json_data["timelines"]['map']
    dataMap = {
        "key": {
            "uuid": timelineUuid
        },
        "value": {
            "@class": "TimelineResourceBase",
            "id": {
                "uuid": timelineUuid
            }
        }
    }
    map.append(dataMap)
    with open(filename,'w+') as file:
        json.dump(json_data, file, indent = 2)
   
    with open(filename,'r+') as file:
        json_data = json.load(file)
        file.close()

    print ("Done insertOwnerLinkToAnimation = " + str(json_data))

def insertOwnerLinkToAnimation(animationsDir, animationType, ownerLink, is_imported, animation, json_data):
    print ("Start insertOwnerLinkToAnimation = " + str(ownerLink))
    json_data['AnimationType'] = animationType
    json_data['OwnerLink'] = ownerLink
    json_data['is_imported'] = is_imported
    print ("Anitmation data = " + str(json_data))
    for filename in animationsDir.iterdir():
        if pathlib.Path(filename).stem != animation:
            continue
        with open(filename,'w+') as file:
            json.dump(json_data, file, indent = 2)
    print ("Done insertOwnerLinkToAnimation = " + str(ownerLink))

def handleSymbolTable(mappingProvider, symbolTable, createUuidExe):
    #if ownerLink
                # 1-> Owner link 
                #    2 Symbol table 
                #        3 Found in "variables" with ownerlink uuid:
                #            4 if found 
                #                5 check name for trigger "name": "trigger__8F14CD62_447A_45B2_968F_717224BA9834__Object1st", 
                #                    6  trigger__8F14CD62_447A_45B2_968F_717224BA9834__Object1st -> uuid
                #                        7 uuid->realUuid
                #                           9   manu -g "trigger__8F14CD62_447A_45B2_968F_717224BA9834__Object1st"
                #                           8 CreateNewWithNameGenerator("trigger__8F14CD62_447A_45B2_968F_717224BA9834__Object1st") -->uuid
    print("!!!! handleSymbolTable = " + str(symbolTable))
    if 'variables' in symbolTable:
        for variables in symbolTable['variables']:
            name = variables["name"]
            if name.startswith("trigger__") :
                print("YEAH!!!!! name = " + str(name))
                string = str(name).split('__')
                uuidExpr = string[1].replace('_', '-')
                print("YEAH!!!!! uuidExpr = " + str(uuidExpr))
                print("YEAH!!!!! mappingProvider = " + str(mappingProvider))
                if "prototypeToInstanceMap" in mappingProvider:
                    for prototypeToInstanceMap in mappingProvider["prototypeToInstanceMap"]:
                        if prototypeToInstanceMap["key"]["uuid"] == uuidExpr :
                            print("CreateUuidExe = " + str(createUuidExe))
                            command = [str(createUuidExe), str(name)]
                            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            outUuid = result.stdout.decode('utf-8')
                            outUuid = outUuid.replace('\r', '')
                            outUuid = outUuid.replace('\n', '')   
                            randomId = str(uuid.uuid4()).upper()
                            dataPrototypeToInstanceMap = {
                                        "key": {
                                        "uuid": str(outUuid).upper()
                                        },
                                        "value": {
                                        "uuid": randomId
                                        }
                                    }
                            mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap)
                            print("YEAH!!!!! found = " + str(outUuid))


    print("!!!! handleSymbolTable done = " + str(symbolTable))

def handleTriggers(mappingProvider, triggers):

    for trigger in triggers:
        randomId = str(uuid.uuid4()).upper()
        realId = trigger['id'] ['uuid']
        dataPrototypeToInstanceMap = {
                    "key": {
                    "uuid": realId
                    },
                    "value": {
                    "uuid": randomId
                    }
                }
        mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap)

        if 'targetBindingLink' in trigger:
            if 'target' in trigger['targetBindingLink']:
                randomId = str(uuid.uuid4()).upper()
                realId = trigger['targetBindingLink']['target']['id']['uuid']
                dataPrototypeToInstanceMap1 = {
                        "key": {
                        "uuid": randomId
                        },
                        "value": {
                        "uuid": realId
                        }
                    }
                trigger['targetBindingLink']['target']['id']['uuid'] = randomId  
                mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap1)
                realOptional = str(uuid.uuid4()).upper()
                print ("!!!!trigger targetBindingLink realOptional= " + str(realOptional))
                optionalId = {
                    "uuid": realOptional
                }
                randomoptionalId = str(uuid.UUID(int=0)).upper()
                dataPrototypeToInstanceMap2 = {
                        "key": {
                        "uuid": realOptional
                        },
                        "value": {
                        "uuid": randomoptionalId
                        }
                    }
                mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap2)
                trigger['targetBindingLink']['target']['optionalId'] = optionalId

        if 'zoneBindingLink' in trigger:
            if 'target' in trigger['zoneBindingLink']:
                randomId = str(uuid.uuid4()).upper()
                realId = trigger['zoneBindingLink']['target']['id']['uuid']
                dataPrototypeToInstanceMap1 = {
                        "key": {
                        "uuid": randomId
                        },
                        "value": {
                        "uuid": realId
                        }
                    }
                trigger['zoneBindingLink']['target']['id']['uuid'] = randomId
                mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap1)
                realOptional =  str(uuid.uuid4()).upper()
                optionalId = {
                    "uuid": realOptional
                }
                randomoptionalId = str(uuid.UUID(int=0)).upper()
                dataPrototypeToInstanceMap2 = {
                        "key": {
                        "uuid": realOptional
                        },
                        "value": {
                        "uuid": randomoptionalId
                        }
                    }
                mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap2)    
                trigger['zoneBindingLink']['target']['optionalId'] = optionalId


def copyOwnerLinkToAnimation(projectDir, animationType, ownerLink, is_imported, animation, mappingProvider, triggers, symbolTable, createUuidExe):
    #print ("Start create copyOwnerLinkToAnimation = " + str(ownerLink) + " animationType =" + str(animationType) + "triggers" + str(triggers))
    #print (animation)
    animationsDir = pathlib.Path(projectDir).joinpath('animations')
    for filename in animationsDir.iterdir():
        if pathlib.Path(filename).stem != animation:
            continue
        print("found animation file = " + str(filename))
        with open(filename,'r+') as file:
            json_data = json.load(file)
            file.close()

            if "target" not in ownerLink :
                randomUuid = str(uuid.uuid4()).upper()
                idData = {
                    "id": {
                        "uuid": randomUuid
                    },
                    "type": 0
                }         
                ownerLink['target'] = idData

            handleTriggers(mappingProvider, triggers)
            handleSymbolTable(mappingProvider, symbolTable, createUuidExe)
            if animationType == 'sky' :
                scriptsDir = pathlib.Path(projectDir).joinpath('scripts')
                for filescript in scriptsDir.iterdir():
                    f = open(filescript)
                    json_data_script = json.load(f)
                    if json_data_script['@class'] == 'Script_SkyBox':
                        print("realUuid from Script_SkyBox = " + str(filescript))
                        realUuid = json_data_script['id']['uuid']
                        randomUuid = str(uuid.uuid4()).upper()
                        if id not in ownerLink :
                            idData = {
                                    "uuid": randomUuid
                            }                
                            ownerLink['target']['id'] = idData
                            
                        ownerLink['target']['id']['uuid'] = randomUuid
                        dataPrototypeToInstanceMap = {
                            "key": {
                            "uuid": randomUuid
                            },
                            "value": {
                            "uuid": realUuid
                            }
                        }
                        mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap)

            if animationType == 'sun' :
                scriptsDir = pathlib.Path(projectDir).joinpath('scripts')
                for filescript in scriptsDir.iterdir():
                    f = open(filescript)
                    json_data_script = json.load(f)
                    if json_data_script['@class'] == 'Script_Sun':
                        print("realUuid from Script_Sun = " + str(filescript))
                        realUuid = json_data_script['id']['uuid']  
                        randomUuid = str(uuid.uuid4()).upper()
                        if id not in ownerLink :
                            idData = {
                                    "uuid": randomUuid
                            }                
                            ownerLink['target']['id'] = idData
                        ownerLink['target']['id']['uuid'] = randomUuid
                        dataPrototypeToInstanceMap = {
                            "key": {
                            "uuid": randomUuid
                            },
                            "value": {
                            "uuid": realUuid
                            }
                        }
                        mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap)

            if animationType == 'timeline' :
                    if 'tracks' in json_data:
                        for tracks in json_data['tracks']:
                                if 'clips' in tracks:
                                    for clip in tracks['clips']:
                                        if 'behavior' in clip:
                                            bindinglink = clip['bindinglink']
                                            bindinglinkUuid = bindinglink['target']['id']['uuid']
                                            randombindinglinkUuid = str(uuid.uuid4()).upper()
                                            dataPrototypeToInstanceMapExpr = {
                                                "key": {
                                                "uuid": randombindinglinkUuid
                                                },
                                                "value": {
                                                "uuid": bindinglinkUuid
                                                }
                                            }
                                            mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMapExpr)
                                            bindinglink['target']['id']['uuid'] = randombindinglinkUuid

            if animationType == 'tagVariable' :
                randomUuid = str(uuid.uuid4()).upper()
                realUuid = ownerLink['target']['optionalId']['uuid']
                dataPrototypeToInstanceMap = {
                    "key": {
                    "uuid": randomUuid
                    },
                    "value": {
                    "uuid": realUuid
                    }
                }
                mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap)

           
            if animationType == 'avar' or  animationType == 'object3D' or  animationType == 'objVariable' or  animationType == 'tag' :  
                realUuid = ownerLink['target']['id']['uuid']
                randomUuid = str(uuid.uuid4()).upper() 
                ownerLink['target']['id']['uuid'] = randomUuid
                dataPrototypeToInstanceMap = {
                    "key": {
                    "uuid": randomUuid
                    },
                    "value": {
                    "uuid": realUuid
                    }
                }
                mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMap)

            

            if 'tracks' in json_data:
               for tracks in json_data['tracks']:
                    if 'clips' in tracks:
                        for clip in tracks['clips']:
                            if 'behavior' in clip:
                                behavior = clip['behavior']                       
                                if 'frames' in behavior:
                                    for frame in behavior['frames']:
                                        if 'formula' in frame:
                                            expr = frame['formula']['expression']
                                            if "__" not in str(expr):
                                                continue
                                            string = str(expr).split('__')
                                            n = len(string)
                                            if n == 2 :
                                                uuidExpr = string[1].replace('_', '-')
                                                dataPrototypeToInstanceMapExpr = {
                                                        "key": {
                                                        "uuid": randomUuid
                                                        },
                                                        "value": {
                                                        "uuid": uuidExpr
                                                        }
                                                    }
                                                mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMapExpr)
                                            else : 
                                                #split string into chunks
                                                results = re.split('[__][__]',str(expr))
                                                print(results)
                                                for res in results:
                                                    print(results)
                                                    uuidCandidate = res.replace('_', '-')
                                                    if is_valid_uuid(uuidCandidate) == 1 :
                                                        randomUuidExpr = str(uuid.uuid4()).upper()
                                                        dataPrototypeToInstanceMapExpr = {
                                                            "key": {
                                                            "uuid": randomUuidExpr
                                                            },
                                                            "value": {
                                                            "uuid": uuidCandidate
                                                            }
                                                        }
                                                        mappingProvider['prototypeToInstanceMap'].append(dataPrototypeToInstanceMapExpr)

        #вставляем новый OwnerLink
        insertOwnerLinkToAnimation(animationsDir, animationType, ownerLink, is_imported, animation, json_data)
        return
       
    print ("Done create copyOwnerLinkToAnimation = ")

def createTimeline(projectDir, timelineUuid, mappingProvider, createUuidExe):
    print ("createTimeline Start create timeline = " + str(timelineUuid))
    scriptsDir = pathlib.Path(projectDir).joinpath('scripts')
    for file in scriptsDir.iterdir():
        if pathlib.Path(file).stem != timelineUuid:
            continue
        f = open(file)
        json_data = json.load(f)        
        if json_data['@class'] != 'TimeLineScript':
            continue 
        print("found base sript file = " + str(file))
        is_imported = json_data['is_imported']      
        loop = json_data['loop']
        triggers = []
        if 'triggers' in json_data:
            triggers = json_data['triggers']

        symbolTable = []
        if 'symbolTable' in json_data:
            symbolTable = json_data['symbolTable']

        priority = 0
        if 'priority' in json_data:
            priority = json_data['priority']
        id = json_data['id']
        animations = [];
        if 'scripts' in json_data:
            for list in json_data['scripts']['list']:
                if list['@class'] != 'AnimationScript':
                    continue 
                data = {
                "animation": list['animation'],
                "isEnabled": list['isEnabled'],
                }
                animations.append(data)
                ownerLink = list['OwnerLink']
                is_importedAnimation = list['is_imported']
                animationType = list['AnimationType']
                # Нужно обновить анимацию, добавить туда OwnerLink
                copyOwnerLinkToAnimation(projectDir, animationType, ownerLink, is_importedAnimation, list['animation']['uuid'], mappingProvider, triggers, symbolTable, createUuidExe)                
        

        timeLinesDir = pathlib.Path(projectDir).joinpath('timelines')
        
        if not os.path.exists(timeLinesDir):
            os.makedirs(timeLinesDir)
            
        fileTimeLines = timeLinesDir.joinpath(timelineUuid)
        fileTimeLinesBase = pathlib.Path(fileTimeLines).stem + ".json"
        fileTimeLinesFull = timeLinesDir.joinpath(fileTimeLinesBase)
        f = open(fileTimeLinesFull, 'w+')
        data = {
            "@class": "TimelineResourceBase",
            "id": id,
            "is_imported": is_imported,
            "loop": loop,
            "priority": priority,
            "triggers":triggers,
            "animations":animations,
            }
        print (data)    
        json.dump(data, f, indent = 2)
        f.close()
        print ("Done create timelines" + str(fileTimeLinesFull) )
        print ("Remove old timelines" + str(file) )
        os.remove(file)

        return
        
    print ("Timelines not created")      

def migrateScene(filename, projectDir, createUuidExe):
    print("Start migrate scene") 
    f = open(filename)
    json_data = json.load(f)

    if 'nodes' not in json_data:
        return
    for node in json_data['nodes']:
        if 'object3D' not in node:
            continue
        object = node['object3D']
        if 'timeline' not in object:
            continue

        timeline = object['timeline']    
        print("found timeline = " + timeline['timelineId']['uuid']+ "for animation = " + object['name'])
        mappingProvider = {
                "@class": "IdPoolBase",
                "prototypeToInstanceMap": []        
        }        
        createTimeline(projectDir, timeline['timelineId']['uuid'], mappingProvider, createUuidExe)
        updateResourcePack(projectDir, timeline['timelineId']['uuid'])
        print("found mappingProvider = " + str(mappingProvider) + "for animation = " + object['name'])
        timeline['mappingProvider'] = mappingProvider
        print("new timeline = " + str(timeline))
        if 'scriptSystem' in json_data:
            scriptSystem = json_data['scriptSystem']
            for scripts in scriptSystem['scripts']:
                uuid = scripts['id']['uuid']
                if uuid == timeline['timelineId']['uuid']:
                    print("scripts uuid = " + str(uuid))
                    scriptSystem['scripts'].remove(scripts)
                    print("scriptSystem= " + str(scriptSystem))

    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent = 2)
        outfile.close()
        
              
    print("Done migrate scene")  
    #with open(filename, 'w') as outfile:
        #json.dump(json_data, outfile, indent = 2)

def migrateProject(projectDir, createUuidExe):
    print("Start migrate project" + createUuidExe) 
    scenesDir = pathlib.Path(projectDir).joinpath('scenes')
    for file in scenesDir.iterdir():
        print("found scene file = "  + str(file))
        if file.is_file() and file.suffix == '.json':
            data = migrateScene(file, projectDir, createUuidExe)
    print("Done migrate project")        
#migrateProject('D:\\pareaManu\\Hectors-Treasure', 'D:\\pareaManu\\manu\\CreateUUIDFromString\\out\\build\\x64-debug\\CreateUUIDFromString\\CreateUUIDFromString')
migrateProject('D:\\pareaManu\\testPro\\EmptyProject-develop', 'D:\\pareaManu\\manu\\CreateUUIDFromString\\out\\build\\x64-debug\\CreateUUIDFromString\\CreateUUIDFromString')
# migrateProject('/Users/ez/Work/manu-projects/matrix_anims')



# files = [
#     'animations/102FA042-03DD-40DD-A78B-4ABB1C6ED6A6.json',
#     'animations/AEFD323D-B94F-40C9-AA2E-002E5D1D7299.json',
#     'animations/E3E0F06D-A9DA-42D1-B9DE-53D611DD3CF9.json',
# ]

# for file in files:
#     data = migrate(file)
#     with open(file, 'w') as outfile:
#         json.dump(data, outfile, indent = 2)