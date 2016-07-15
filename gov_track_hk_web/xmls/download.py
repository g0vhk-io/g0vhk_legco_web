# -*- coding: utf-8 -*-
import requests
year_range = ["12-13", "13-14", "14-15", "15-16"]
meeting_types = ["cm", "esc", "pwsc", "hc", "fc"]
url_format = {"cm": "http://www.legco.gov.hk/yr%s/chinese/counmtg/voting/cm_vote_", "esc": "http://www.legco.gov.hk/yr%s/chinese/fc/esc/results/esc_vote_", "pwsc": "http://www.legco.gov.hk/yr%s/chinese/fc/pwsc/results/pwsc_vote_", "hc": "http://www.legco.gov.hk/yr%s/chinese/hc/voting/hc_vote_", "fc": "http://www.legco.gov.hk/yr%s/chinese/fc/fc/results/fc_vote_"}
detect_url_format = "http://www.legco.gov.hk/php/detect-votes.php?term=yr%s&meeting=%s"
for yr in year_range:
    for mc in meeting_types:
        detect_url = detect_url_format % (yr, mc)
        r = requests.get(detect_url)
        print(detect_url)
        xml_files = [f for f in r.text.split(",") if f.endswith(".xml")]
        print(xml_files)
        for xml_file in xml_files:
            download_url = url_format[mc] % (yr) + xml_file
            xml_r = requests.get(download_url)
            xml_r.encoding = 'utf-8'
            f = open(mc + "_" + xml_file, "wb")
            f.write(xml_r.text.encode("utf-8"))
            f.close()

