import json

from translator.Translators import FIELD_REFERENCES
from translator.Translators import GLOBAL_TABLE_IGNORE,SQL_TYPE
from translator.translator_funcs import *

class JSON_SQL:
    ################################################################
    #
    # If sql_types is empty assume all columns are varchar(string).
    # If list is [(None,None),(
    #
    def __init__(self, table_name, json_text ):
        ############################################################
        #
        # Expect a list of dictionaries [ {},{},{} ] OR
        # with the newer version we can have [{ {},{},{}}, etc}. IOW a
        # dict of dicts for for a dict like {'id':123, name:{'en','foo'}}
        # the columns id and name.en would be created.
        #
        try:
            self.json_data = json.loads(json_text)
        except TypeError as te:
            self.json_data = json_text # See if the text to data has occured
        
        self.cols = []
        self.table_name = table_name
        self.MAP_DELIMITER='__'

        tmp=None
        for d in self.json_data: # Get a row of data
            self._column_name(d, self.cols)
            
            # print(self.cols)
    
    def _column_name(self, json_dict, cols, prefix=''):
        # Now check if the sub data is a type or another dict
        for k in [k for k in  json_dict.keys()]:
            # Check if the json data contains another DICT
            if isinstance(json_dict[k],dict):
                # Yes, now mangle the map with the class delimiter
                self._column_name(json_dict[k],
                                  cols=cols,
                                  prefix=prefix+k+self.MAP_DELIMITER)
            else:
                # I automatically create an ID as primary key so I need to
                # mangle the id if it has one in the json data!
                if k.upper() == 'ID':
                    k='data_id'
                # Just add the data key and move on
                if prefix+k not in cols:
                    cols.append(prefix+k)
                    
    def table_create_sql(self):
        statement = 'CREATE TABLE ' + self.table_name + '( id SERIAL NOT NULL, '
        for column_name in self.cols:
            if column_name in GLOBAL_TABLE_IGNORE[self.table_name]: continue
            try:
                sql_type = FIELD_REFERENCES[column_name][SQL_TYPE]
                statement = statement + column_name + ' ' + sql_type + ','
            except KeyError as ke:
                statement = statement + column_name + ' ' + 'varchar' + ','
        statement = statement + 'PRIMARY KEY( id ));'
        # Load any additional table create statements here
        return statement
    
    def table_drop_sql(self):
        statement = 'DROP TABLE ' + self.table_name + ' CASCADE;'
        return statement

    def create_inserts(self):
        ret_val=[]
        for jd in self.json_data:
            ############################################################
            #
            # Assume a dictionary of datathat maps to the already created
            # columns
            #
            cols = [k for k in self.cols]

            statement = 'INSERT INTO ' + self.table_name + ' ('
            for c in self.cols:
                if c in GLOBAL_TABLE_IGNORE[self.table_name]: continue
                statement = statement + c + ','
            # Remove trailing comma and space
            statement = statement[:-1] + ')'
            statement = statement + ' VALUES ( '

            for c in cols:

                if c in GLOBAL_TABLE_IGNORE[self.table_name]: continue                
                value = None
                
                for k in c.split(self.MAP_DELIMITER):

                    if c == 'data_id': k = 'id'

                    try:
                        if value is None:
                            value = jd[k]
                        else:
                            value = value[k]
                    except KeyError as ke:
                        value = None
                # Gotta unmagle the data_id
                statement = statement+\
                    self._assemble_field( value ) + ", "
                    
            # Remove the trainling comma and space
            statement = statement[:-2] + ');'
            ret_val.append( statement )
        return ret_val

    def _assemble_field(self, field_val):
        ret_val = field_val
        if ret_val is None:
            ret_val = 'NULL'
        elif str(ret_val) == '-':
            ret_val = 'NULL'
        elif str(ret_val) == '--':
            ret_val = 'NULL'
        elif isinstance( ret_val, str ):
            ret_val = ret_val
            ret_val = ret_val.replace("'","")
            ret_val = "'" + ret_val + "'"
        # To do, need to insert the text from a list by concatinating it
        # then putting in quotes
        elif isinstance( ret_val, type([]) ):
            ret_val = str(field_val[RAW_VAL_POS])
            ret_val = ret_val.replace("'","")
            ret_val = "'" + ret_val + "'"
        else:
            # Assume here that everything is a number (float or int)
            ret_val = str(ret_val)
            return ret_val
        return ret_val
            
