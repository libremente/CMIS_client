""" Client to connect to a remote CMIS server and perform operations """ 
# pylint: disable=C0103

# Imports
from cmislib import CmisClient

def changeUrl(singleChild): 
    """ Check for a path and update with new one """
    toCheck = '/modules'
    newOne = '/old'
    cmisField = 'fr:campo'
    needle = 'needle'
    # Get the field
    properties = singleChild.getProperties()
    field = properties[cmisField]
    print(field)

    if( needle in field and newOne not in field):
        print ('Old field: %s' , field)
        position = field.find(toCheck)
        newUrl = field[:position] + newOne + field[position:]
        print ('New field: %s', newUrl)
        newField = {cmisField : newUrl}
        singleChild.updateProperties(newField)
        print("Done")
        
def main():
    """ Main function """
    # Read info from file
    filename = 'local_settings'

    # Open file
    try:
        with open(filename) as fileIn:
            lines = fileIn.readlines()
    except EnvironmentError:
        print ("Settings file does not exist!")
        exit(1)

    # Set the variables
    # File with 4 lines, info on each.
    try:
        repository = lines[0].rstrip('\n')
        user = lines[1].rstrip('\n')
        password = lines[2].rstrip('\n')
        # Target folder name
        folder = lines[3].rstrip('\n')
    except Exception as e:
        print ('Error reading file')
        exit(1)

    # Connect to the repository
    try:
        print(repository, user, password)
        repository = CmisClient(repository, user, password)
      
        if not repository:
            print ('Error retrying info from repository.Exiting.')
            exit(1)

        print ('Connected to repository')
        # Get the default repository
        repo = repository.defaultRepository
        if not repo:
            print ('Error retrying info from repository.Exiting.')
            exit(1)

        print(repo)
        # Query folder 
        robotResults = repo.getObjectByPath(folder)

        print ('Looking inside %s folder' , folder)
        # Print name of contents in folder
        children = robotResults.getChildren()

        if not children:
            print ("Error while retrying results! Exiting...")
            exit(1)

        # Loop and print
        i = 0 
        for child in children:
            print ("Item: %s is called %s" % (i, child.name))

            # Get object's properties
            childProperties = child.getProperties()
            # Now I want to check the StreamMimeType
            stream = childProperties['cmis:contentStreamMimeType']
            # If framemaker, do something
            if( 'framemaker' in stream):
                changeUrl(child)
            i = i + 1

    except Exception as e:
        print ('There is an error connecting to the repo')
        print(e)

# Call main
main()
