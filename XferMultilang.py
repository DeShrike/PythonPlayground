'''

USE [ABCDE_NatchOS]

SELECT ML.[LabelID]
	  ,L.Name
      ,ML.[LCID]
      ,ML.[Text]
	  ,isnull(ML.updatetime,isnull(ML.creationtime, isnull(L.Updatetime,l.Creationtime))) AS LastModification
  FROM CMS.MultilangLabel L
  LEFT OUTER JOIN CMS.MultilangLabelML ML ON L.LabelID = ML.LabelID
  WHERE isnull(ML.updatetime,isnull(ML.creationtime, isnull(L.Updatetime,l.Creationtime))) > '2018-01-01'
  AND ML.Text <> '' AND ML.Text IS NOT NULL
  ORDER BY isnull(ML.updatetime,isnull(ML.creationtime, isnull(L.Updatetime,l.Creationtime))) DESC, ML.LCID  


Voor bovenstaande SELECT uit op 'source' Server. (STAGING)
Bewaar resultaten in bestand "staging.txt"	(zie hieronder)
Verwijder de eerste lijn (headers)
Zorg dat de file enkel labels bevat waarvan de tekst geen CRLF's bevat ! Een label mag dus niet wrappen.
Voor dit python script uit:
	python XferMultilang.py > out.sql
Paste de inhoud van out.sql in MSSMS
Zie ook onderaan het script (ROLLBACK / COMMIT ! select one)

'''

##################################################################################################################

labelsFilename = 'outilfr.txt'

##################################################################################################################

def ProcessLine(line):
	parts = line.split("\t")
	value = parts[3]
	if (value == ""):
		return;
	value = value.replace("'", "''")
	print("-- STAGING ID: #%s - %s" % (parts[0], parts[1]))

	print("DECLARE @id int;")
	print("DECLARE @lcid int;")
	print("DECLARE @name nvarchar(100);")
	print("DECLARE @value nvarchar(4000);")
	print("DECLARE @oldvalue nvarchar(4000);")
	print("DECLARE @lastmod datetime;")
	print("DECLARE @livelastmod datetime;")
	print("SET @lcid = %s;" % parts[2])
	print("SET @lastmod = CONVERT(datetime,'%s');" % parts[4][:19])
	print("SET @name = '%s';" % parts[1])
	print("SET @value = '%s';" % value)
	print("""		
	SELECT @id = LabelID FROM CMS.MultilangLabel WHERE Name = @name;
	IF (@id IS NULL)
	BEGIN
		PRINT 'INSERTING MultilangLabel ' + @name;
		INSERT INTO CMS.MultilangLabel(Name, IsSystem, IsMultiLine, CreationTime)
	    	VALUES (@name, 0, 0, GETDATE());
		SET @id = SCOPE_IDENTITY();
	END;
	PRINT 'LIVE ID = ' + STR(@id);
	IF EXISTS (SELECT * FROM CMS.MultilangLabelML WHERE LabelID = @id AND LCID = @lcid)
	BEGIN
		SELECT @livelastmod = isnull(ML.updatetime, isnull(ML.creationtime, isnull(L.Updatetime, L.Creationtime))),
			@oldvalue = ML.[Text]
			FROM CMS.MultilangLabel L
			INNER JOIN CMS.MultilangLabelML ML ON L.LabelID = ML.LabelID
			WHERE L.LabelID = @id AND ML.LCID = @lcid;
		IF (@livelastmod < @lastmod)
		BEGIN
			PRINT 'Updating Label ' + @name + ' for ' + STR(@lcid);
			PRINT '** OLD: ' + @oldvalue;
			PRINT '** NEW: ' + @value;
			UPDATE CMS.MultilangLabelML SET [Text] = @value, UpdateTime = GETDATE() WHERE LabelID = @id AND LCID = @lcid;
		END
		ELSE
		BEGIN	
			PRINT 'LIVE Version Modified on ' + CONVERT(nvarchar(max), @livelastmod) + ' and STAGING Version on ' + CONVERT(nvarchar(max), @lastmod);
		END;
	END
	ELSE
	BEGIN
		PRINT 'Inserting Label ' + @name + ' for ' + STR(@lcid);
		INSERT INTO CMS.MultilangLabelML (LabelID, LCID, [Text], CreationTime )
	    	VALUES (@id, @lcid, @value, GETDATE());
	END;
	GO

	""")

##################################################################################################################

def ReadLines():
	file = open(labelsFilename, "r") 
	for line in file:
		ProcessLine(line)
	file.close()

##################################################################################################################
##################################################################################################################
##################################################################################################################
# main()
##################################################################################################################
if __name__ == "__main__":
	print("")
	print("")
	print("-- TODO: enter databasename")
	print("USE [ABCDE_NatchOS]")
	print("")
	print("BEGIN TRANSACTION lalabels")
	print("")
	print("")
	ReadLines()
	print("")
	print("")
	print("-- TODO: select one")
	print("-- ROLLBACK TRANSACTION lalabels")
	print("-- COMMIT TRANSACTION lalabels")

##################################################################################################################
##################################################################################################################
