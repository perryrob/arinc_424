
from spec.arinc_424_18_parser import ARINC_FIELD_NAME, FIELD_REFERENCE, IGNORE
from spec.arinc_424_18_parser import SQL_TABLE, ADDITIONAL_SQL_LIST, SQL_DEF
from translator.Translators import SQL_TYPE

from parser.Parser import COLUMN_NAME_POS,RAW_VAL_POS, TRANSLATED_VAL_POS

import psycopg2

class DB_ARINC_Tables:

    def __init__(self,
                 section_subsections,
                 arinc_424_parse_def,
                 field_references):
        self.section_subsections = section_subsections
        self.arinc_424_parse_def = arinc_424_parse_def
        self.field_references = field_references

    def table_create_sql(self):
        self.create_table_statements=[]
        for section, subsection in self.section_subsections:
            arinc_table_def = self.arinc_424_parse_def[section][subsection]
            table_name = arinc_table_def[SQL_DEF][SQL_TABLE]
            statement = 'CREATE TABLE ' + table_name + '( id integer, '
            for column in arinc_table_def[1:]:
                column_name = column[ARINC_FIELD_NAME]

                if column_name in IGNORE: continue
                
                field_ref = column[FIELD_REFERENCE]
                sql_type = self.field_references[field_ref][SQL_TYPE]
                statement = statement + column_name + ' ' + sql_type + ','
            statement = statement + 'PRIMARY KEY( id ) '
            # Load any additional table create statements here
            for additional_statement in \
                arinc_table_def[SQL_DEF][ADDITIONAL_SQL_LIST]:
                statement = statement + additional_statement

            statement = statement + ');'
            
            self.create_table_statements.append(statement)
        return self.create_table_statements

    def table_drop_sql(self):
        self.create_table_statements=[]
        for section, subsection in self.section_subsections:
            arinc_table_def = self.arinc_424_parse_def[section][subsection]
            table_name = arinc_table_def[SQL_DEF][SQL_TABLE]
            statement = 'DROP TABLE ' + table_name + ' CASCADE;'
            self.create_table_statements.append(statement)
        return self.create_table_statements

class DB_ARINC_data:
    def __init__(self,section_subsections,arinc_424_parse_def,records={}):
        self.records = records
        self.section_subsections = section_subsections
        self.arinc_424_parse_def = arinc_424_parse_def
        self.index=0

    def create_inserts(self):
        self.insert_statements=[]
        for section, subsection in self.section_subsections:
            arinc_table_def = self.arinc_424_parse_def[section][subsection]
            records = self.records[(section,subsection)]
            table_name = arinc_table_def[SQL_DEF][SQL_TABLE]
            # Form the table column names for the insert statemetn
            for record in records:
                # There are currently 3 assumed columns outside of the
                # ARINC spec used to link up the data. It is id.
                statement = 'INSERT INTO ' + table_name + ' ( id, '
                for field_val in record:
                    statement = statement + field_val[COLUMN_NAME_POS] + ", "
                # Remove trailing comma and space
                statement = statement[:-2] + ' )'
                # Form the values part tof the insert statement
                statement = statement + ' VALUES ( ' +\
                    str(self.index) + ','
                for field_val in record:
                    statement = statement+\
                        self._assemble_field( field_val ) + ", "
                # Remove the trainling comma and space
                statement = statement[:-2] + ');'
                # Append this insert to the rest of the insert statements
                self.insert_statements.append(statement)
                # add one to the index to support inserting the ID
                self.index = self.index + 1
                
        return self.insert_statements

    def _assemble_field(self, field_val):
        # This value is the translated value after parsing
        ret_val = field_val[TRANSLATED_VAL_POS]                
        if ret_val is None:
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

    
class DB_connect:

    def __init__(self, host='localhost',
                 database='arinc_424',
                 user='perryr',
                 password='peer',
                 debug=False):
        try:
            self.con = psycopg2.connect(dbname=database,
                                        user=user,
                                        password=password)
            if debug:
                cur = self.con.cursor()
                print('PostgresSQL version:')
                cur.execute('select version()')
                version = cur.fetchone()
                print(version)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_connection(self):
        return self.con

    def exec(self, statement, commit=True):
        cur=None
        try:
            cur = self.con.cursor()
            cur.execute( statement )
            if commit:
                self.con.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print( statement )
            print( error )
            cur.execute('rollback;')
            if commit:
                self.con.commit()
            cur.close()
            raise( error )
    
    def exec_from_list(self, statements=[], commit=True):
        count = 0
        try:
            for statement in statements:
                cur = self.con.cursor()
                cur.execute( statement )
                count = count + 1
                cur.close()
            if commit:
                self.con.commit()            
        except (Exception, psycopg2.DatabaseError) as error:
            print( error )
            raise( error )
        
        return count
    
    def commit(self):
        try:
            self.con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            raise( error )
    def close(self):
        try:
            self.con.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print( error )
            raise( error )

