W, ST, MT = "Wood and building", "Stone and glass", "Metal and tools"
HUT, CT = "Colony huts", "Colony tools and storage"
CR, AE, PW, MK = "Create", "AE2", "Powah", "Mekanism"
MC, CP, BP = "Machines and pipes", "Computers and peripherals", "Backpacks and drawers"
BT = "Building tools"
FD = "Food and research items"

def L(grp, *pairs):
    return [(s, r, grp) for s, r in pairs]

WANT = []
WANT += L(W, ("planks", "minecraft:oak_planks"), ("stick", "minecraft:stick"), ("slab", "minecraft:oak_slab"), ("stairs", "minecraft:oak_stairs"),
          ("fence", "minecraft:oak_fence"), ("fence_gate", "minecraft:oak_fence_gate"), ("door", "minecraft:oak_door"), ("trapdoor", "minecraft:oak_trapdoor"),
          ("ladder", "minecraft:ladder"), ("sign", "minecraft:oak_sign"), ("chest", "minecraft:chest"), ("barrel", "minecraft:barrel"),
          ("crafting_table", "minecraft:crafting_table"), ("bed", "minecraft:white_bed"), ("torch", "minecraft:torch"),
          ("chest_boat", "minecraft:oak_chest_boat"), ("boat", "minecraft:oak_boat"), ("white_banner", "minecraft:white_banner"))
WANT += L(ST, ("furnace", "minecraft:furnace"), ("stone", "minecraft:stone"), ("smooth_stone", "minecraft:smooth_stone"), ("stone_bricks", "minecraft:stone_bricks"),
          ("stone_brick_slab", "minecraft:stone_brick_slab"), ("stone_brick_stairs", "minecraft:stone_brick_stairs"), ("stone_brick_wall", "minecraft:stone_brick_wall"),
          ("cobble_slab", "minecraft:cobblestone_slab"), ("cobble_stairs", "minecraft:cobblestone_stairs"), ("cobble_wall", "minecraft:cobblestone_wall"),
          ("glass", "minecraft:glass"), ("glass_pane", "minecraft:glass_pane"))
WANT += L(MT, ("iron_ingot", "minecraft:iron_ingot"), ("gold_ingot", "minecraft:gold_ingot"), ("copper_ingot", "minecraft:copper_ingot"),
          ("iron_nugget", "minecraft:iron_nugget"), ("iron_block", "minecraft:iron_block"), ("iron_bars", "minecraft:iron_bars"), ("chain", "minecraft:chain"),
          ("lantern", "minecraft:lantern"), ("iron_pickaxe", "minecraft:iron_pickaxe"), ("iron_axe", "minecraft:iron_axe"), ("iron_hoe", "minecraft:iron_hoe"),
          ("iron_sword", "minecraft:iron_sword"), ("stone_pickaxe", "minecraft:stone_pickaxe"), ("stone_axe", "minecraft:stone_axe"), ("stone_hoe", "minecraft:stone_hoe"),
          ("wooden_pickaxe", "minecraft:wooden_pickaxe"), ("wooden_axe", "minecraft:wooden_axe"), ("wooden_hoe", "minecraft:wooden_hoe"),
          ("shears", "minecraft:shears"), ("fishing_rod", "minecraft:fishing_rod"), ("bow", "minecraft:bow"), ("iron_boots", "minecraft:iron_boots"),
          ("leather_boots", "minecraft:leather_boots"), ("redstone_block", "minecraft:redstone_block"), ("zinc_ingot", "alltheores:zinc_ingot"), ("zinc_nugget", "alltheores:zinc_nugget"),
          ("osmium_ingot", "alltheores:osmium_ingot"), ("tin_ingot", "alltheores:tin_ingot"), ("dust_copper", "mekanism:dust_copper"), ("dust_gold", "mekanism:dust_gold"), ("dust_iron", "mekanism:dust_iron"), ("dust_refined_obsidian", "mekanism:dust_refined_obsidian"), ("iron_helmet", "minecraft:iron_helmet"), ("iron_chestplate", "minecraft:iron_chestplate"),
          ("iron_leggings", "minecraft:iron_leggings"), ("shield", "minecraft:shield"), ("bucket", "minecraft:bucket"))
HUTS = ["alchemist", "archery", "baker", "barracks", "beekeeper", "blacksmith", "builder", "chickenherder", "citizen", "combatacademy", "composter", "concretemixer", "cook",
        "cowboy", "crusher", "deliveryman", "dyer", "enchanter", "farmer", "fisherman", "fletcher", "florist", "gatehouse", "glassblower", "graveyard", "guardtower",
        "hospital", "kitchen", "library", "lumberjack", "mechanic", "miner", "mysticalsite", "netherworker", "plantation", "sawmill", "school", "shepherd", "sifter",
        "smeltery", "stable", "stonemason", "stonesmeltery", "swineherder", "tavern", "townhall", "university", "warehouse"]
WANT += [("hut_" + h, "minecolonies:blockhut" + h, HUT) for h in HUTS]
WANT += L(HUT, ("hut_field", "minecolonies:blockhutfield"), ("hut_plantation_field", "minecolonies:blockhutplantationfield"))
WANT += L(CT, ("build_tool", "structurize:sceptergold"), ("scan_tool", "structurize:sceptersteel"), ("clipboard", "minecolonies:clipboard"),
          ("resource_scroll", "minecolonies:resourcescroll"), ("build_goggles", "minecolonies:build_goggles"), ("supply_camp", "minecolonies:supplycampdeployer"),
          ("supply_ship", "minecolonies:supplychestdeployer"), ("rack", "minecolonies:blockminecoloniesrack"), ("postbox", "minecolonies:blockpostbox"),
          ("stash", "minecolonies:blockstash"), ("architects_cutter", "domum_ornamentum:architectscutter"))
WANT += L(CR, ("andesite_alloy", "create:andesite_alloy"), ("shaft", "create:shaft"), ("cogwheel", "create:cogwheel"), ("large_cogwheel", "create:large_cogwheel"),
          ("andesite_casing", "create:andesite_casing"), ("water_wheel", "create:water_wheel"), ("mechanical_press", "create:mechanical_press"),
          ("mechanical_mixer", "create:mechanical_mixer"), ("whisk", "create:whisk"), ("basin", "create:basin"), ("mechanical_drill", "create:mechanical_drill"),
          ("crushing_wheel", "create:crushing_wheel"), ("encased_fan", "create:encased_fan"), ("propeller", "create:propeller"), ("belt_connector", "create:belt_connector"),
          ("chute", "create:chute"), ("millstone", "create:millstone"), ("depot", "create:depot"), ("empty_blaze_burner", "create:empty_blaze_burner"),
          ("brass_ingot", "create:brass_ingot"), ("iron_sheet", "create:iron_sheet"), ("copper_sheet", "create:copper_sheet"), ("golden_sheet", "create:golden_sheet"),
          ("goggles", "create:goggles"), ("brass_casing", "create:brass_casing"), ("super_glue", "create:super_glue"), ("windmill_bearing", "create:windmill_bearing"),
          ("sail_frame", "create:sail_frame"), ("gearbox", "create:gearbox"), ("andesite_funnel", "create:andesite_funnel"), ("track", "create:track"),
          ("track_station", "create:track_station"), ("train_controls", "create:controls"), ("railway_casing", "create:railway_casing"))
WANT += L(AE, ("certus_dust", "ae2:certus_quartz_dust"), ("silicon", "ae2:silicon"), ("printed_calc", "ae2:printed_calculation_processor"),
          ("printed_eng", "ae2:printed_engineering_processor"), ("printed_logic", "ae2:printed_logic_processor"), ("printed_silicon", "ae2:printed_silicon"),
          ("calc_processor", "ae2:calculation_processor"), ("eng_processor", "ae2:engineering_processor"), ("logic_processor", "ae2:logic_processor"),
          ("charged_certus", "ae2:charged_certus_quartz_crystal"), ("fluix_dust", "ae2:fluix_dust"), ("fluix_crystal", "ae2:fluix_crystal"), ("inscriber", "ae2:inscriber"), ("charger", "ae2:charger"),
          ("growth_accelerator", "ae2:growth_accelerator"), ("quartz_glass", "ae2:quartz_glass"), ("controller", "ae2:controller"), ("drive", "ae2:drive"),
          ("energy_acceptor", "ae2:energy_acceptor"), ("energy_cell", "ae2:energy_cell"), ("item_cell_housing", "ae2:item_cell_housing"),
          ("cell_component_1k", "ae2:cell_component_1k"), ("cell_component_4k", "ae2:cell_component_4k"), ("item_storage_cell_1k", "ae2:item_storage_cell_1k"),
          ("item_storage_cell_4k", "ae2:item_storage_cell_4k"), ("terminal", "ae2:terminal"), ("crafting_terminal", "ae2:crafting_terminal"),
          ("pattern_encoding_terminal", "ae2:pattern_encoding_terminal"), ("blank_pattern", "ae2:blank_pattern"), ("crafting_storage_1k", "ae2:1k_crafting_storage"),
          ("crafting_storage_4k", "ae2:4k_crafting_storage"), ("crafting_accelerator", "ae2:crafting_accelerator"), ("crafting_unit", "ae2:crafting_unit"),
          ("pattern_provider", "ae2:pattern_provider"), ("molecular_assembler", "ae2:molecular_assembler"), ("annihilation_core", "ae2:annihilation_core"),
          ("formation_core", "ae2:formation_core"), ("me_interface", "ae2:interface"), ("import_bus", "ae2:import_bus"), ("export_bus", "ae2:export_bus"),
          ("storage_bus", "ae2:storage_bus"), ("fluix_glass_cable", "ae2:fluix_glass_cable"), ("fluix_covered_cable", "ae2:fluix_covered_cable"),
          ("fluix_covered_dense_cable", "ae2:fluix_covered_dense_cable"), ("p2p_tunnel", "ae2:me_p2p_tunnel"), ("wireless_access_point", "ae2:wireless_access_point"),
          ("wireless_booster", "ae2:wireless_booster"), ("meteorite_compass", "ae2:meteorite_compass"))
WANT += L(PW, ("dielectric_paste", "powah:dielectric_paste"), ("dielectric_casing", "powah:dielectric_casing"), ("energizing_orb", "powah:energizing_orb"),
          ("energizing_rod_starter", "powah:energizing_rod_starter"), ("energy_cable_starter", "powah:energy_cable_starter"), ("powah_energy_cell_starter", "powah:energy_cell_starter"),
          ("furnator_starter", "powah:furnator_starter"), ("magmator_starter", "powah:magmator_starter"), ("thermo_generator_starter", "powah:thermo_generator_starter"),
          ("solar_panel_starter", "powah:solar_panel_starter"), ("steel_energized", "powah:steel_energized"), ("crystal_blazing", "powah:crystal_blazing"),
          ("ender_cell_starter", "powah:ender_cell_starter"), ("reactor_starter", "powah:reactor_starter"), ("energy_cable_basic", "powah:energy_cable_basic"),
          ("furnator_basic", "powah:furnator_basic"), ("powah_energy_cell_basic", "powah:energy_cell_basic"), ("capacitor_basic_tiny", "powah:capacitor_basic_tiny"))
WANT += L(MK, ("metallurgic_infuser", "mekanism:metallurgic_infuser"), ("steel_casing", "mekanism:steel_casing"), ("steel_ingot", "mekanism:ingot_steel"),
          ("enriched_carbon", "mekanism:enriched_carbon"), ("enriched_iron", "mekanism:enriched_iron"), ("basic_control_circuit", "mekanism:basic_control_circuit"),
          ("advanced_control_circuit", "mekanism:advanced_control_circuit"), ("alloy_infused", "mekanism:alloy_infused"), ("alloy_reinforced", "mekanism:alloy_reinforced"),
          ("alloy_atomic", "mekanism:alloy_atomic"), ("energy_tablet", "mekanism:energy_tablet"), ("basic_energy_cube", "mekanism:basic_energy_cube"),
          ("basic_universal_cable", "mekanism:basic_universal_cable"), ("enrichment_chamber", "mekanism:enrichment_chamber"), ("purification_chamber", "mekanism:purification_chamber"),
          ("chemical_injection_chamber", "mekanism:chemical_injection_chamber"), ("electrolytic_separator", "mekanism:electrolytic_separator"),
          ("chemical_infuser", "mekanism:chemical_infuser"), ("energized_smelter", "mekanism:energized_smelter"), ("crusher", "mekanism:crusher"),
          ("electric_pump", "mekanism:electric_pump"), ("digital_miner", "mekanism:digital_miner"), ("quantum_entangloporter", "mekanism:quantum_entangloporter"),
          ("basic_tier_installer", "mekanism:basic_tier_installer"), ("speed_upgrade", "mekanism:upgrade_speed"), ("energy_upgrade", "mekanism:upgrade_energy"),
          ("thermal_evaporation_block", "mekanism:thermal_evaporation_block"), ("thermal_evaporation_controller", "mekanism:thermal_evaporation_controller"),
          ("thermal_evaporation_valve", "mekanism:thermal_evaporation_valve"), ("dynamic_tank", "mekanism:dynamic_tank"))
WANT += L(MC, ("iron_furnace", "ironfurnaces:iron_furnace"), ("pipez_item_pipe", "pipez:item_pipe"), ("pipez_basic_upgrade", "pipez:basic_upgrade"), ("pipez_wrench", "pipez:wrench"), ("pipez_improved_upgrade", "pipez:improved_upgrade"), ("pipez_advanced_upgrade", "pipez:advanced_upgrade"),
          ("laser_node", "laserio:laser_node"), ("laser_wrench", "laserio:laser_wrench"), ("laser_connector", "laserio:laser_connector"),
          ("laser_card_item", "laserio:card_item"), ("laser_filter_basic", "laserio:filter_basic"))
WANT += L(CP, ("computer_advanced", "computercraft:computer_advanced"), ("colony_integrator", "advancedperipherals:colony_integrator"), ("me_bridge", "advancedperipherals:me_bridge"),
          ("peripheral_casing", "advancedperipherals:peripheral_casing"))
WANT += L(BP, ("backpack", "sophisticatedbackpacks:backpack"), ("pickup_upgrade", "sophisticatedbackpacks:pickup_upgrade"), ("magnet_upgrade", "sophisticatedbackpacks:magnet_upgrade"),
          ("upgrade_base", "sophisticatedbackpacks:upgrade_base"), ("drawer_1x1", "functionalstorage:oak_1"), ("storage_controller", "functionalstorage:storage_controller"),
          ("warp_stone", "waystones:warp_stone"), ("waystone", "waystones:waystone"), ("warp_dust", "waystones:warp_dust"))

WANT += L(BT, ("nature_compass", "naturescompass:naturescompass"), ("destruction_gadget", "buildinggadgets2:gadget_destruction"), ("exchanging_gadget", "buildinggadgets2:gadget_exchanging"),
          ("copy_paste_gadget", "buildinggadgets2:gadget_copy_paste"), ("cut_paste_gadget", "buildinggadgets2:gadget_cut_paste"), ("charging_station", "charginggadgets:charging_station"),
          ("copper_stick", "constructionstick:copper_stick"), ("iron_stick", "constructionstick:iron_stick"), ("diamond_stick", "constructionstick:diamond_stick"),
          ("mega_torch", "torchmaster:megatorch"), ("coal_block", "minecraft:coal_block"), ("gold_block", "minecraft:gold_block"))

WANT += L(FD, ("steak", "minecraft:cooked_beef"), ("cooked_chicken", "minecraft:cooked_chicken"), ("cake", "minecraft:cake"), ("cookie", "minecraft:cookie"),
          ("golden_carrot", "minecraft:golden_carrot"), ("brick", "minecraft:brick"), ("chiseled_stone_bricks", "minecraft:chiseled_stone_bricks"),
          ("anvil", "minecraft:anvil"), ("lead", "minecraft:lead"), ("rail", "minecraft:rail"))

WANT += L(FD, ("flint_knife", "farmersdelight:flint_knife"), ("cutting_board", "farmersdelight:cutting_board"), ("cooking_pot", "farmersdelight:cooking_pot"))
MA = "Mystical Agriculture"
WANT += L(MA, ("infusion_altar", "mysticalagriculture:infusion_altar"), ("infusion_pedestal", "mysticalagriculture:infusion_pedestal"),
          ("infusion_crystal", "mysticalagriculture:infusion_crystal"), ("inferium_seeds", "mysticalagriculture:inferium_seeds"),
          ("inferium_farmland", "mysticalagriculture:inferium_farmland"), ("prosperity_seed_base", "mysticalagriculture:prosperity_seed_base"),
          ("prosperity_ingot", "mysticalagriculture:prosperity_ingot"))
FX = "Flux Networks"
WANT += L(FX, ("flux_core", "fluxnetworks:flux_core"), ("flux_controller", "fluxnetworks:flux_controller"), ("flux_plug", "fluxnetworks:flux_plug"),
          ("flux_point", "fluxnetworks:flux_point"), ("flux_configurator", "fluxnetworks:flux_configurator"))
WANT += L(MC, ("sophisticatedstorage_barrel", "sophisticatedstorage:barrel"), ("hopper", "minecraft:hopper"))

BP, MG, PB = "Botany Pots", "Mob Grinding Utils", "Productive Bees"
WANT += L(BP, ("botany_pot", "botanypots:terracotta_botany_pot"), ("hopper_botany_pot", "botanypots:terracotta_hopper_botany_pot"))
WANT += L(MG, ("mgu_spikes", "mob_grinding_utils:spikes"), ("mgu_fan", "mob_grinding_utils:fan"), ("mgu_entity_conveyor", "mob_grinding_utils:entity_conveyor"),
          ("mgu_absorption_hopper", "mob_grinding_utils:absorption_hopper"), ("mgu_tinted_glass", "mob_grinding_utils:tinted_glass"), ("mgu_saw", "mob_grinding_utils:saw"))
WANT += L(PB, ("honey_treat", "productivebees:honey_treat"), ("advanced_oak_beehive", "productivebees:advanced_oak_beehive"), ("oak_wood_nest", "productivebees:oak_wood_nest"),
          ("stone_nest", "productivebees:stone_nest"), ("centrifuge", "productivebees:centrifuge"), ("bee_cage", "productivebees:bee_cage"),
          ("beehive", "minecraft:beehive"), ("campfire", "minecraft:campfire"))
WANT += L(MT, ("block_gen_stone", "cobblegengalore:block_gen_stone"))

# registry id / tag -> slug, for ingredients that stand for a generic thing
MAP = {
    "#minecraft:planks": "planks", "#minecraft:logs": "log", "#minecraft:logs_that_burn": "log", "#minecraft:oak_logs": "log", "#c:stripped_logs": "log", "#c:stripped_woods": "log",
    "#c:rods/wooden": "stick", "#c:rods": "stick", "#minecraft:wooden_slabs": "slab", "#minecraft:wooden_doors": "door", "#minecraft:wooden_trapdoors": "trapdoor",
    "#minecraft:stone_crafting_materials": "cobblestone", "#c:cobblestones": "cobblestone", "#c:cobblestones/normal": "cobblestone", "minecraft:cobblestone": "cobblestone",
    "#c:stones": "stone", "#c:stones/stone": "stone",
    "#minecraft:smelts_to_glass": "sand", "#c:sands": "sand", "#c:sands/colorless": "sand", "minecraft:sand": "sand",
    "#c:ingots/iron": "iron_ingot", "#c:nuggets/iron": "iron_nugget", "#c:storage_blocks/iron": "iron_block", "#c:plates/iron": "iron_sheet",
    "#c:ingots/gold": "gold_ingot", "#c:ingots/copper": "copper_ingot", "#c:plates/gold": "golden_sheet", "#c:plates/copper": "copper_sheet",
    "#c:raw_materials/iron": "raw_iron", "minecraft:raw_iron": "raw_iron", "#c:raw_materials/gold": "raw_gold", "minecraft:raw_gold": "raw_gold",
    "#c:raw_materials/copper": "raw_copper", "minecraft:raw_copper": "raw_copper", "#c:ores/iron": "raw_iron", "#c:ores/gold": "raw_gold", "#c:ores/copper": "raw_copper",
    "#c:strings": "string", "minecraft:string": "string", "#c:glass_blocks": "glass", "#c:glass_blocks/colorless": "glass", "#c:chests": "chest", "#c:chests/wooden": "chest",
    "#minecraft:chest_boats": "chest_boat", "#minecraft:boats": "boat", "#c:slimeballs": "slime_ball", "#c:slime_balls": "slime_ball", "#c:netherracks": "netherrack",
    "#c:gems/diamond": "diamond", "minecraft:diamond": "diamond", "#c:dusts/redstone": "redstone", "minecraft:redstone": "redstone",
    "minecraft:coal": "coal", "#minecraft:coals": "coal", "#c:gems/coal": "coal", "minecraft:charcoal": "coal",
    "minecraft:andesite": "andesite", "minecraft:quartz": "nether_quartz", "#c:gems/quartz": "nether_quartz",
    "ae2:certus_quartz_crystal": "certus_quartz", "#c:gems/certus_quartz": "certus_quartz",
    "#c:wool": "wool", "#minecraft:wool": "wool",
    "#c:storage_blocks/redstone": "redstone_block", "#c:drinks/milk": "milk_bucket", "#c:eggs": "egg", "#c:storage_blocks/coal": "coal_block", "#c:storage_blocks/gold": "gold_block", "#saplings": "sapling", "#minecraft:saplings": "sapling", "#logs": "log", "#c:ender_pearls": "ender_pearl", "#mekanism:tin": "tin_ingot", "#c:dusts/copper": "dust_copper", "#c:ingots/tin": "tin_ingot", "#ae2:all_nether_quartz": "nether_quartz", "#ae2:all_certus_quartz": "certus_quartz", "#ae2:all_fluix": "fluix_crystal", "#c:dusts/fluix": "fluix_dust", "minecraft:ender_pearl": "ender_pearl",
    "#c:glass_blocks/cheap": "glass", "#c:glass_panes": "glass_pane", "#c:glass_panes/colorless": "glass_pane", "#c:leathers": "leather", "#c:feathers": "feather",
    "#c:buckets/empty": "bucket", "#c:hives": "beehive", "#c:campfires": "campfire", "#c:honeycombs": "honeycomb", "minecraft:honeycomb": "honeycomb", "minecraft:honey_bottle": "honey_bottle", "#c:tools/shear": "shears", "#c:buckets/water": "water_bucket", "minecraft:farmland": "farmland", "#c:buckets/lava": "lava_bucket", "#c:dusts/glowstone": "glowstone_dust", "#c:gems/emerald": "emerald", "#c:gems/lapis": "lapis_lazuli",
    "#c:obsidians/normal": "obsidian", "#c:obsidians": "obsidian", "#c:rods/blaze": "blaze_rod", "#c:ingots/zinc": "zinc_ingot", "#c:nuggets/zinc": "zinc_nugget",
    "#c:dusts/gold": "dust_gold", "#c:dusts/iron": "dust_iron", "#c:ingots/osmium": "osmium_ingot", "#c:ingots/steel": "steel_ingot", "#c:ingots/vibranium": "vibranium_ingot",
    "#c:ingots/bronze": "bronze_ingot", "#c:circuits/basic": "basic_control_circuit", "#c:gems/amethyst": "amethyst_shard", "#c:crops/wheat": "wheat",
    "minecraft:kelp": "kelp", "minecraft:gravel": "gravel", "minecraft:flint": "flint", "minecraft:redstone_block": "redstone_block", "minecraft:slime_ball": "slime_ball",
    "#mekanism:carbon": "coal", "#mekanism:redstone": "redstone", "#mekanism:diamond": "diamond", "#mekanism:refined_obsidian": "dust_refined_obsidian",
}
# things you gather rather than craft (their texts live in the page)
LEAF = {k: "" for k in ["sapling", "chicken", "milk_bucket", "cocoa_beans", "nether_wart", "rabbit_foot", "saddle", "gilded_blackstone", "wheat_seeds", "leather", "wheat", "apple", "egg", "beef", "porkchop", "bone", "flint", "gravel", "dirt", "honeycomb", "obsidian", "blaze_rod", "amethyst_shard", "ender_pearl",
                        "feather", "sugar_cane", "lapis_lazuli", "poppy", "carrot", "cactus", "kelp", "glowstone_dust", "emerald", "lava_bucket", "raw_zinc", "raw_osmium", "clay_ball", "vibranium_ingot", "raw_tin", "uraninite", "sky_stone_block",
                        "raw_tin", "uraninite", "sky_stone_block", "silicon_press", "calculation_processor_press", "engineering_processor_press", "logic_processor_press", "water_bucket", "rabbit_hide", "honey_bottle","log", "cobblestone", "sand", "raw_iron", "raw_copper", "raw_gold", "redstone", "coal", "diamond", "string", "wool", "andesite", "certus_quartz",
                        "nether_quartz", "slime_ball", "netherrack", "inferium_essence", "prosperity_shard", "flux_dust", "farmland", "bone", "flint", "honey_bottle"]}
ALLOW = {"minecraft", "create", "ae2", "mekanism", "powah", "minecolonies", "structurize", "ironfurnaces", "pipez", "laserio", "functionalstorage", "sophisticatedbackpacks",
         "advancedperipherals", "computercraft", "waystones", "domum_ornamentum", "kubejs", "alltheores", "allthemodium",
         "farmersdelight", "mysticalagriculture", "fluxnetworks", "sophisticatedstorage", "botanypots", "mob_grinding_utils", "productivebees", "cobblegengalore"}
PICK = {"cake": "farmersdelight:cake_from_milk_bottle", "dielectric_rod": "powah:crafting/dielectric_rod", "dielectric_rod_horizontal": "powah:crafting/dielectric_rod_h", "fluix_crystal": "ae2:transform/fluix_crystals", "iron_ingot": "minecraft:iron_ingot_from_smelting_raw_iron", "gold_ingot": "minecraft:gold_ingot_from_smelting_raw_gold", "copper_ingot": "minecraft:copper_ingot_from_smelting_raw_copper"}
