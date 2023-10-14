import xml.etree.ElementTree as ET

def parse_robot_output(file_path):
    # Dictionary to hold parsed data
    suites = []
    current_suite = None
    current_test = None

    # Iterating through the XML elements as they're encountered
    for event, elem in ET.iterparse(file_path, events=('start', 'end')):
        if event == 'start':
            if elem.tag == 'suite':
                suite_name = elem.attrib.get('name', 'Unnamed Suite')
                current_suite = {
                    'name': suite_name,
                    'tests': []
                }
            elif elem.tag == 'test':
                test_name = elem.attrib.get('name', 'Unnamed Test')
                current_test = {
                    'name': test_name,
                    'status': None,
                    'keywords': []
                }
            elif elem.tag == 'kw':
                keyword_name = elem.attrib.get('name', 'Unnamed Keyword')
                current_keyword = {
                    'name': keyword_name,
                    'status': None
                }
                if current_test:  # Assuming keywords are always within tests
                    current_test['keywords'].append(current_keyword)

        if event == 'end':
            if elem.tag == 'status':
                if current_test and not current_test['status']:
                    current_test['status'] = elem.attrib['status']
                elif current_keyword and not current_keyword['status']:
                    current_keyword['status'] = elem.attrib['status']
            elif elem.tag == 'test':
                current_suite['tests'].append(current_test)
                current_test = None
            elif elem.tag == 'suite':
                suites.append(current_suite)
                current_suite = None

            # Clear the element from memory to keep memory usage low
            elem.clear()

    return suites