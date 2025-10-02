# BTMoreArmor
BattleTech more that adds armor to mech

# How to use
1. First you need to copy all the chassisdefs you have:
   1. BattleTech_Data/StreamingAssets/data/chassis/ - Base game path. Don't copy ChassisTemplate.json and chassisdef_*_TESTDUMMY.json.
   2. DLC data can be found here: https://github.com/caardappel-hbs/ Download and copy chassis folder. Only download if you own those DLCs.
      1. *DLC*/data/chassis/
   3. Modes. Run the game once with Modtek installed. Go to .modtek/Cache/ folder and copy ChassisDef folder.
2. Now you should have 5 sub folders: Base, Flashpoint, HeavyMetal, UrbanWarfare, Mods. Only the first is required. The rest are optional.
3. Use the main script to change the armor values. A new subfolder for the mod will be created. Just copy it to your mod folder. Modtek will do the rest
4. Don't forget: This mod requires all of my other mods. 
5. Search your mod folder for mod.json files containing "ChassisDef" string (case doesn't matter) and add to mod.json "DependsOn" every mod that has these files.
   6. "DependsOn" should look like "DependsOn": ["HeatAndWeight", "mode1", "mode2", "mode3"]
   7. Included mod.json includes the mods I have. Might be ok for you too.
   8. Mod name is inside the mod.json file. 