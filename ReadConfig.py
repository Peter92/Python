def read_config(config_filename, config_sections=None, update_values=False):
    Config = ConfigParser.ConfigParser()
    Config.optionxform = str
    Config.read(config_filename)
    if config_sections is not None:
        with open(config_filename, 'r+') as f:
            for new_section in config_sections:
                try:
                    Config.add_section(new_section)
                except ConfigParser.DuplicateSectionError:
                    pass
                section_items = config_sections[new_section]
                for new_item in section_items:
                    prefix = {float: 'f', int: 'i', bool: 'b'}.get(type(section_items[new_item]), 'u')
                    item_name = prefix + new_item[0].upper() + new_item[1:]
                    try:
                        Config.get(new_section, item_name)
                        if update_values:
                            raise ConfigParser.NoOptionError(item_name, new_section)
                    except ConfigParser.NoOptionError:
                        Config.set(new_section, item_name, str(section_items[new_item]))
            Config.write(f)
            
    prefixes = {'f': Config.getfloat, 'i': Config.getint, 'b': Config.getboolean}
    config_dict = {}
    for section in Config.sections():
        config_dict[section] = {}
        for item in Config.options(section):
            config_dict[section][item[1:]] = prefixes.get(item[0], Config.get)(section, item)
    return config_dict
