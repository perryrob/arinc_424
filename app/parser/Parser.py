
from spec.arinc_424_18_parser import ARINC_424_PARSE_DEF
from spec.arinc_424_18_parser import ARINC_FIELD_NAME,ARINC_FIELD_WIDTH,\
    SECTION_CODE, SUBSECTION_CODE, FIELD_REFERENCE, IGNORE

from translator.Translators import TRANSLATOR_FUNC

COLUMN_NAME_POS=0
RAW_VAL_POS=1
TRANSLATED_VAL_POS=2

class RecordParser:

    def __init__(self, ARINC_file, parse_sections=[], stats={},
                 field_translators=None):
        self.inf = open( ARINC_file,'r' )
        self.count = 0
        self.record_objs = {}
        self.stats = stats
        self.parse_sections = parse_sections
        self.field_translators = field_translators
        self._parse()

    def _parse(self):
        
        with self.inf as arinc_data:
            for data_line in arinc_data:
                tokens=[]
                section, sub_section = \
                    self.get_record_section_subsection( data_line,tokens )
                if len(tokens) > 0:
                    if (section,sub_section) in self.record_objs.keys():         
                        self.record_objs[(section,sub_section)].append( tokens )
                    else:
                        self.record_objs[(section,sub_section)] = []
                        self.record_objs[(section,sub_section)].append( tokens ) 
        self.inf.close()

    def get_record_section_subsection(self, data_line, tokens):
        parse_def = ARINC_424_PARSE_DEF[' ']
        start_parse=0
        internal_tokens = {}
        section_code = ''
        sub_section_code = ''
        # Take a first pass and get the Section Code
        for token_parse in parse_def:
            field_name = token_parse[ARINC_FIELD_NAME]
            end_parse = start_parse + token_parse[ARINC_FIELD_WIDTH]
            internal_tokens[field_name] = str(data_line[start_parse:end_parse])
            start_parse = end_parse
        # If this is an S record, figure out the sub section
        if internal_tokens['ST'] == 'S':
            section_code = internal_tokens[SECTION_CODE]
            section_field_def = ARINC_424_PARSE_DEF[section_code]
            # Now just pick any subsection and parse the first 10 tokens to
            # get the subsection. I believe that any subsection definition
            # will contain the subsection in the correct position
            subsection_field_def = list(section_field_def.values())[0]
            # Now iterate the first section definition to see which subsection
            # to use
            start_parse=0
            # subsection definition is sliced. The first record is reserved
            # for the database table name.
            for i in range(1,10):
                token_parse = subsection_field_def[i]
                field_name = token_parse[ARINC_FIELD_NAME]
                end_parse = start_parse + token_parse[ARINC_FIELD_WIDTH]
                if field_name == SUBSECTION_CODE:
                    sub_section_code = \
                        str(data_line[start_parse:end_parse]) # Do not use strip
                    break
                start_parse = end_parse
            # Let's do some BS detection here. Check the section and sub section
            # keys to make sure they exist. If the section is a P and the sub
            # section is an N, the subsection is in a different location and
            # needs special handling. Stupid SPEC!
            section_subsection_def = []
            if (section_code in ARINC_424_PARSE_DEF.keys()) and \
               (sub_section_code in ARINC_424_PARSE_DEF[section_code].keys()):
                pass
            else:
                # The outlier! Airport / Terminal NDB
                section_code = 'P'
                sub_section_code = 'N'
            section_subsection_def = \
                ARINC_424_PARSE_DEF[section_code][sub_section_code]
            # Moving the filter down here to speed up parsing
            if len(self.parse_sections) != 0 and \
               (section_code,sub_section_code) not in self.parse_sections:
                return section_code,sub_section_code
            
            # Now that we know the section and subsection we can parse the data
            # line and load the values. Note that up to this point data_line
            # is just iterated and not changed. Not that the section/
            start_parse=0
            # subsection definition is sliced. The first record is reserved
            # for the database table name.
            for token_parse in section_subsection_def[1:]:

                end_parse = start_parse + token_parse[ARINC_FIELD_WIDTH]
                
                field_name = token_parse[ARINC_FIELD_NAME]

                # Do not strip
                # Get the name of the translator from the token_parse object
                # and send that into translate_filed with the parsed variable
                # to translate the val into a usable value.
                field_val = str(data_line[start_parse:end_parse])
                start_parse = end_parse

                # There are some fields I do not want in the DB
                if field_name in IGNORE: continue

                translator_tup = None
                translator_field_val = None
                try:                    
                    translator_tup= self.translator_field_lookup(
                        token_parse[FIELD_REFERENCE])
                except NameError as ne:
                    print( ne )
                    print( data_line )
                    print( token_parse )
                    raise( ne)                    

                try:
                    # Try to translate the field
                    translated_field_val = self.translate_field(
                        translator_tup[TRANSLATOR_FUNC],
                        field_val )
                except ValueError as ve:
                    print( ve )
                    print( data_line )
                    print( token_parse )
                    raise(ve)
                except TypeError as te:
                    print( te )
                    print( data_line )
                    print( token_parse )
                    raise(te)

                
                tokens.append(
                    [ field_name,
                      field_val,
                      translated_field_val]
                )
                # Update the start from the end of the last field
        return section_code,sub_section_code

    def get_records(self):
        return self.record_objs

    def translator_field_lookup(self, field_reference):
        if self.field_translators is None:
            return None
        
        field_translator_name = \
            self.field_translators.field_reference_parse_lookup(
                field_reference
            )

        return field_translator_name
        
    
    def translate_field(self, translator, val ):
        if self.field_translators is None:
            return val
        return translator(val)
