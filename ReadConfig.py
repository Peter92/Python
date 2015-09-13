def read_config(config_filename, config_sections=None, write_values=False, update_values=False):
    
    #Create config instance
    Config = ConfigParser.ConfigParser()
    Config.optionxform = str
    Config.read(config_filename)
    
    #Capitalise section names
    if config_sections is not None:
        config_sections = {join_words(k): v for k, v in config_sections.iteritems()}
    
    #Write/update INI file
    if config_sections is not None and write_values:
        
        #Detect if file exists
        try:
            with open(config_filename, 'r'):
                open_method = 'r+'
        except IOError:
            open_method = 'w'
            
        with open(config_filename, open_method) as f:
            for new_section in config_sections:
                
                #Add section
                try:
                    Config.add_section(new_section)
                except ConfigParser.DuplicateSectionError:
                    pass
                    
                section_items = config_sections[new_section]
                for new_item in section_items:
                    
                    #Change name to reflect the type
                    prefix = {float: 'f', int: 'i', bool: 'b'}.get(type(section_items[new_item]), 'u')
                    item_name = prefix + join_words(new_item)
                    
                    #Add to config
                    try:
                        Config.get(new_section, item_name)
                        if update_values:
                            raise ConfigParser.NoOptionError(item_name, new_section)
                    except ConfigParser.NoOptionError:
                        Config.set(new_section, item_name, str(section_items[new_item]))
                        
            Config.write(f)
    
    #Read file contents
    prefixes = {'f': Config.getfloat, 'i': Config.getint, 'b': Config.getboolean}
    config_dict = {}
    for section in Config.sections():
        config_dict[section] = {}
        for item in Config.options(section):
            config_dict[section][item[1:]] = prefixes.get(item[0], Config.get)(section, item)
    
    #Update contents if values haven't been added
    if not write_values and config_sections is not None:
        config_sections = {k: {join_words(k2): (str(v2) if type(v2) not in (float, int, bool) else v2) for k2, v2 in v.iteritems()} for k, v in config_sections.iteritems()}
        config_dict.update(config_sections)
        
    return config_dict
