# 1F_import
importing data from csv

## project structure
**1F_import/**  
&nbsp;&nbsp;&nbsp;&nbsp; 1_map_builder.py  
&nbsp;&nbsp;&nbsp;&nbsp; 2_sender_id_getter.py  
&nbsp;&nbsp;&nbsp;&nbsp; 3_xml_builder.py  
&nbsp;&nbsp;&nbsp;&nbsp; 4_import.py  
&nbsp;&nbsp;&nbsp;&nbsp; **database/**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; xml.pdl  
&nbsp;&nbsp;&nbsp;&nbsp; **input/** *-- data file (.csv)*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; input_file.csv  
&nbsp;&nbsp;&nbsp;&nbsp; **logs/**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; log.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; wrong_soates.txt  
&nbsp;&nbsp;&nbsp;&nbsp; **results/** *-- generated data*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; data.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; map.py  
&nbsp;&nbsp;&nbsp;&nbsp; **sources/**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; areas.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; connection_strings.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; constants.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; db.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; receiver_identifiers.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sender_identifiers.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; serv.py  
&nbsp;&nbsp;&nbsp;&nbsp; **templates/** *-- form section templates*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; section_1.xml  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; section_2.xml  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ...  
