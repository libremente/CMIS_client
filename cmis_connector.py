#   CMIS Client connects to a CMIS repo and performs CRUD actions.
#    Copyright (C) 2018  libremente 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

""" Client to connect to a remote CMIS server and perform operations """ 
# pylint: disable=C0103

# Imports
from cmislib import CmisClient
import json

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
    filename = 'config.json'

    # Open file
    try:
        with open(filename) as fileIn:
            data = json.load(fileIn)
    except EnvironmentError:
        print ("Settings file does not exist!")
        exit(1)

    # Set the variables
    # File with 4 lines, info on each.
    try:
        repository = data['repository'] 
        user = data['user'] 
        password = data['password'] 
        folder = data['folder'] 
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
        repoResults = repo.getObjectByPath(folder)

        print ('Looking inside %s folder' , folder)
        # Print name of contents in folder
        children = repoResults.getChildren()

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
