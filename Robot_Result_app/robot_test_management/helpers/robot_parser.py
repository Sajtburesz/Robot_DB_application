import xml.etree.ElementTree as ET
from datetime import datetime
from django.utils import timezone
from rest_framework import serializers

def parse_date(date_string):
    for fmt in ["%Y%m%d %H:%M:%S.%f", "%Y%m%dT%H%M%S.%f", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise serializers.ValidationError(f"Date format for {date_string} not recognized.")

def parse_robot_output(xml_file):
    results = []
    current_suite = None
    executed_at = None
    robot_tag_found = False

    for event, elem in ET.iterparse(xml_file, events=('start', 'end')):
        if event == 'start' and elem.tag == 'robot':
            robot_tag_found = True
            generated = elem.get("generated")
            executed_at = parse_date(generated)
            executed_at = timezone.make_aware(executed_at, timezone.utc)
            continue
        
        if not robot_tag_found:
            raise serializers.ValidationError("The provided file is not a Robot Framework test result file.")
        
        if event == 'start' and elem.tag == 'suite':
            current_suite = {"name": elem.get("name"), "tests": []}
            
        elif event == 'end' and elem.tag == 'test':
            status_elem = elem.find('status')

            starttime = status_elem.get('starttime') if status_elem is not None else None
            endtime = status_elem.get('endtime') if status_elem is not None else None
            duration = None

            if starttime and endtime:
                start_dt = parse_date(starttime)
                end_dt = parse_date(endtime)
                duration = (end_dt - start_dt).total_seconds()
            testcase_data = {
                'name': elem.get('name'),
                'status': status_elem.get('status') if status_elem is not None else None,
                'duration': duration,
            }
            
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
                
            elem.clear()
        
        elif event == 'end' and elem.tag == 'suite':
            if current_suite and current_suite["tests"]:
                results.append(current_suite)
            current_suite = None
    
    return results, executed_at


