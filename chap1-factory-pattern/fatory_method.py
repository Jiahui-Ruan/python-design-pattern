import xml.etree.ElementTree as etree
import json

class JSONConnector(object):

    def __init__(self, filepath):
        self.data = dict()
        self.filepath = filepath
        with open(filepath, mode='r') as f:
            self.data = json.load(f)
    @property
    def parsed_data(self):
        return self.data

class XMLConnector(object):

    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree

def connection_fatory(filepath):
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError('Cannot connect to {}'.format('filepath'))
    return connector(filepath)

def connect_to(filepath):
    factory = None
    try:
        factory = connection_fatory(filepath)
    except ValueError as ve:
        print ve
    return factory

def main():
    sqlite_factory = connect_to('data/person.sq3')
    print ''

    xml_factory = connect_to('data/person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(".//{}[{}='{}']".format('person', 'lastName', 'Liar'))
    print 'found: {} persons'.format(len(liars))
    for liar in liars:
        print 'first name: {}'.format(liar.find('firstName').text)
        print 'last name: {}'.format(liar.find('lastName').text)
        for p in liar.find('phoneNumbers'): print 'phone number ({}):'.format(p.attrib['type'], p.text)
    print ''

    json_factory = connect_to('data/dount.json')
    json_data = json_factory.parsed_data
    print 'found: {} dounts'.format(len(json_data))
    for dount in json_data:
        print 'name: {}'.format(dount['name'])
        print 'price: ${}'.format(dount['ppu'])
        for t in dount['topping']: print 'topping: {} {}'.format(t['id'], t['type'])

if __name__ == '__main__':
    main()
