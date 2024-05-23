import requests, json
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import  urljoin
import re

HTML = """
<ul>
    <li class="org-list">
        <a href=https://vaww.va.gov/health/>Veterans Health Administration</a>
        <br>
        With 152 VA medical centers (VAMCs) nationwide, VHA manages
        one of the largest health care systems in the United States. VAMCs within
        a Veterans Integrated Service Network (VISN) work together to provide efficient,
        accessible health care to veterans in their areas. The VHA also conducts research
        and education, and provides emergency medical preparedness.
    </li>
    <li class="org-list">
        <a href=https://vbaw.vba.va.gov/>Veterans Benefits Administration</a>
        <br>
        VBA provides benefits and services to the veteran population
        through 56 VA regional offices. Some of the benefits and services provided
        by VBA to veterans and their dependents include compensation and pension,
        education, loan guaranty, and insurance.
    </li>
    <li class="org-list">
        <a href=https://vaww.nca.va.gov/>National Cemetery Administration</a>
        <br>
        NCA is responsible for providing burial benefits to veterans
        and eligible dependents. The delivery of these benefits involves managing
        141 National Cemeteries nationwide, providing grave markers worldwide, administering
        the State Cemetery Grants Program that complements the National Cemeteries
        network, and providing Presidential Memorial Certificates to next of kin of
        deceased veterans.
    </li>
    <li class="org-list">
        <a href=https://vaww.va.gov/employee/>VA Office of Human Resources and Administration/Operations, Security, and Preparedness (HRA/OSP)</a>
        <br>
        HRA/OSP's functional areas include human resources management, administrative policies and functions, equal opportunity policies and functions, and security and law enforcement.
    </li>
    <li class="org-list">
        <a href=https://vaww.oit.va.gov/>Office of Information and Technology</a>
        <br>
        Information technology is at the core of everything we do at VA and the Office of Information and Technology is tasked with ensuring that VA has the IT tools and services needed to support our Nation's Veterans.
    </li>
    <li class="org-list">
        <a href="/bca/">Board of Contract Appeals</a>
        <br>
        The Department of Veterans Affairs Board of Contract Appeals
        considers and determines appeals from decisions of contracting officers pursuant
        to the Contract Disputes Act of 1978.
    </li>
    <li class="org-list">
        <a href=https://www.bva.va.gov/>Board of Veterans' Appeals</a>
        <br>
        The Board reviews benefit claims determinations made by local
        VA offices and issues decision on appeals. The Board members, attorneys experienced
        in veterans law and in reviewing benefit claims, are the only ones who can
        issue Board decisions.
    </li>
    <li class="org-list">
        <a href="/centerforminorityveterans/">Center for Minority Veterans</a>
        <br>
        As a Center for Excellence, the Center for Minority Veterans
        will ensure that the VA addresses the unique circumstances and special needs
        of minority veterans.
    </li>
    <li class="org-list">
        <a href="/womenvet/">Center for Women Veterans</a>
        <br>
        The mission of the Center for Women Veterans is to ensure
        women veterans have access to VA benefits and services, to ensure that VA
        health care and benefits programs are responsive to the gender-specific needs
        of women veterans, to perform outreach to improve women veterans awareness
        of VA services, benefits and eligibility, and to act as the primary advisor
        to the Secretary for Veterans Affairs on all matters related to programs,
        issues, and initiatives for and affecting women veterans.
    </li>
    <li class="org-list">
        <a href=https://vaww.oalc.va.gov/ >Office of Acquisition, Logistics, and Construction (OALC)</a>
        <br>
        OALC supports the VA administrations and staff offices by providing innovative
        business solutions in the area of acquisition, distribution of supplies, and
        cost effective strategies in asset management and major construction. OALC has
        three major offices, the <a href=https://vaww.va.gov/oal/index.asp title="Office of Acquisition and Logistics">Office of Acquisition and Logistics</a>, the <a href=https://vaww.va.gov/opal/index.asp title="Office of Procurement, Acquisition and Logistics">Office of Procurement, Acquisition and Logistics</a>, and the <a href=http://vaww.cfm.va.gov title="Office of Construction and Facilities Management">Office of Construction and Facilities Management</a>.
    </li>
    <li class="org-list">
        <a href="/adr/">Office of Alternate Dispute Resolution (ADR) and&nbsp; Mediation</a>
        <br>
        This office provides effective training and consulting in
        conflict resolution and ADR (emphasizing mediation) to VA organizations and
        employees.
    </li>
    <li class="org-list">
        <a href=https://www.va.gov/om/index.asp>Office of Management (OM)</a>
        <br>
        OM enables VA to provide a full range of benefits and services to our Nation's Veterans by providing strategic and operational leadership in <a href=https://vaww.va.gov/budget/index.asp>budget</a>, <a href=https://vaww.va.gov/oaem/index.asp>asset enterprise management</a>, <a href=https://vaww.va.gov/finance/index.asp>financial management</a>, <a href=https://vaww.va.gov/fmbts/index.asp>financial management business transformation service</a>, actuarial services, and business oversight. It also promotes public confidence in the Department through stewardship and oversight of business activities that are consistent with national policy, law, and regulation.
    </li>
    <li class="org-list">
        <a href="/oca/">Office of Congressional and Legislative Affairs</a>
        <br>
        The Office of Congressional and Legislative Affairs is the principal point of contact between the Department and Congress and is the oversight and coordinating body for the Department's Congressional relations. The office serves in an advisory capacity to the Secretary and Deputy Secretary as well as other VA managers concerning policies, programs, and legislative matters in which Congressional committees or individual members of Congress have expressed an interest.
    </li>
    <li class="org-list">
        <a href=https://www.oedca.va.gov/>Office of Employment Discrimination Complaint Adjudication</a>
        <br>
        OEDCA maintains a high quality and high performing workforce
        and ensures fairness, integrity, and trust throughout the complaint adjudication
        phase of the Equal Employment Opportunity complaint resolution process.
    </li>
    <li class="org-list">
        <a href=https://vaww.execsec.va.gov/>Office of the Executive Secretary</a>
        <br>
        The Office of the Executive Secretary, a component of the Office of the Secretary,
        serves as the Department's central coordinating point for all documents flowing in and out of the Office of the Secretary.
    </li>
    <li class="org-list">
        <a href=https://dvagov.sharepoint.com/sites/OGC-Client>Office of General Counsel</a>
        <br>
        The General Counsel provides legal advice and services to the Secretary (SECVA) and all organizational components of the Department. The General Counsel is, by statute, the Department's Chief Legal Officer.
    </li>
</ul>
"""

soup = BeautifulSoup(HTML, "html.parser")
data = {}

for item in soup.find_all('li'):
    # name is inside the link
    name = item.find('a').text
    # remove other elements before parsing text
    item.find('a').decompose()
    item.find('br').decompose()
    # process text
    desc = item.text
    desc = desc.replace('\n', '') 
    desc = re.sub(' +', ' ', desc)
    data[name] = desc

with open('departments.json', 'w+') as file:
    json.dump( data, file )