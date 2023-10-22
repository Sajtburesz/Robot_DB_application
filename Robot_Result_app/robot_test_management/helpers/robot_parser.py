import xml.etree.ElementTree as ET

def parse_robot_output(xml_file):
    results = []
    current_suite = None
    
    for event, elem in ET.iterparse(xml_file, events=('start', 'end')):
        
        # If we're starting a new suite
        if event == 'start' and elem.tag == 'suite':
            current_suite = {"name": elem.get("name"), "tests": []}
            
        # If we're ending a test
        elif event == 'end' and elem.tag == 'test':
            status_elem = elem.find('status')
            testcase_data = {
                'name': elem.get('name'),
                'status': status_elem.get('status') if status_elem is not None else None,
            }
            
            # If the test case has failed, extract the failed keywords
            if testcase_data['status'] == 'FAIL':
                testcase_data['keywords'] = []
                for keyword in elem.findall('kw'):
                    keyword_status_elem = keyword.find('status')
                    if keyword_status_elem is not None and keyword_status_elem.get('status') == 'FAIL':
                        keyword_data = {
                            'name': keyword.get('name'),
                            'status': keyword_status_elem.get('status'),
                            'doc': keyword.get('doc'),
                            'log_message': [msg.text for msg in keyword.findall('msg') if msg.text is not None]
                        }
                        testcase_data['keywords'].append(keyword_data)
                
            current_suite["tests"].append(testcase_data)
                
            # Clearing the element from memory
            elem.clear()
        
        # If we're ending a suite
        elif event == 'end' and elem.tag == 'suite':
            if current_suite and current_suite["tests"]:
                results.append(current_suite)
            current_suite = None
    
    return results


