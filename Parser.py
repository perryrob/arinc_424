
from Record import RecordType
from NavAid import Navaid,VHF,NDB
from Route import Enroute,Waypoint,Airway
from Port import Airport
from arinc_424_18_parser import ARINC_424_PARSE_DEF
from arinc_424_18_parser import ARINC_FIELD_NAME,ARINC_FIELD_WIDTH,\
    FIELD_TRANSLATOR
    
class RecordParser:

    def __init__(self, ARINC_file, parse_sections=[], stats={} ):
        self.inf = open( ARINC_file,'r' )
        self.count = 0
        self.record_objs = []
        self.stats = stats
        self.parse_sections = parse_sections
        self._parse()

    def _parse(self):
        
        with self.inf as arinc_data:
            for data_line in arinc_data:
                tokens=[]
                section, sub_section = \
                    self.get_record_section_subsection( data_line,tokens )
                if len(self.parse_sections) == 0:
                    self.record_objs.append( tokens )
                elif (section,sub_section) in self.parse_sections:
                    self.record_objs.append( tokens )
                elif section in self.parse_sections:
                    self.record_objs.append( tokens )
                
        self.inf.close()

    def get_record_section_subsection(self, data_line,tokens=[]):
        parse_def = ARINC_424_PARSE_DEF['']
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
            section_code = internal_tokens['SectionCode']
            section_field_def = ARINC_424_PARSE_DEF[section_code]
            # Now just pick any subsection and parse the first 10 tokens to
            # get the subsection. I believe that any subsection definition
            # will contain the subsection in the correct position
            subsection_field_def = list(section_field_def.values())[0]
            # Now iterate the first section definition to see which subsection
            # to use
            start_parse=0
            for i in range(0,10):
                token_parse = subsection_field_def[i]
                field_name = token_parse[ARINC_FIELD_NAME]
                end_parse = start_parse + token_parse[ARINC_FIELD_WIDTH]
                if field_name == 'SubSectionCode':
                    sub_section_code = \
                        str(data_line[start_parse:end_parse]).strip()
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
            # Now that we know the section and subsection we can parse the data
            # line and load the values. Note that up to this point data_line
            # is just iterated and not changed.
            start_parse=0
            for token_parse in section_subsection_def:
                field_name = token_parse[ARINC_FIELD_NAME]
                end_parse = start_parse + token_parse[ARINC_FIELD_WIDTH]
                tokens.append(
                    [ field_name,
                      str(data_line[start_parse:end_parse]),
                      token_parse[FIELD_TRANSLATOR]]
                )
                start_parse = end_parse            
        return section_code,sub_section_code

    def get_records(self):
        return self.record_objs
            
