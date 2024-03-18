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
        # Expect a list of dictionaries [ {},{},{} ]
        #
        try:
            self.json_data = json.loads(json_text)
        except TypeError as te:
            self.json_data = json_text # See if the text to data has occured
        
        self.cols = None
        self.table_name = table_name
        
        for d in self.json_data:
            if self.cols is None:
                self.cols = [k for k in  d.keys()]
                continue            
            for k in d.keys():
                if k in self.cols:
                    continue
                self.cols.apppend(k)

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
            cols = [k for k in jd.keys()]
            statement = 'INSERT INTO ' + self.table_name + ' ('
            for c in cols:
                if c in GLOBAL_TABLE_IGNORE[self.table_name]: continue
                statement = statement + c + ','
            # Remove trailing comma and space
            statement = statement[:-1] + ')'
            statement = statement + ' VALUES ( '

            for c in cols:
                if c in GLOBAL_TABLE_IGNORE[self.table_name]: continue
                statement = statement+\
                    self._assemble_field( jd[c] ) + ", "
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
            
