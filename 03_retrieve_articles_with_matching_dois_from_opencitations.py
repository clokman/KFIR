"""
Retrieves all articles from OpenCitations that has the same DOI with the records in VU and UvA bibliographies.
"""

# parse list from file (probably exists in ListData)
from retriever.sparql_tools import Open_Citations_Query
from meta.consoleOutput import ConsoleOutput
from preprocessor.string_tools import String

console = ConsoleOutput('log.txt')

doi_list = []
with open('Input//all_dois_in_uva_and_vu_bibliographies.csv', encoding='utf8') as doi_file:
    for each_line in doi_file:
        each_line = String(each_line)
        each_line.clean_from_newline_characters()
        doi_list.append(str(each_line))

oc_query = Open_Citations_Query()
oc_query.retrieve_articles_by_dois(doi_list, show_progress_bar=True)
oc_query.write_results_to_csv('Input//oc_articles_with_matching_dois_v1.3.csv')




# A demo list with 100 DOIs
# doi_list = ['10.1163/187607508X384689', '10.1017/S0954579416000572', '10.1007/s11562-016-0353-7', '10.1016/j.adolescence.2016.09.008', '10.1186/s13561-016-0122-6', '10.1007/s00799-016-0182-6', '10.5194/gmd-2016-266', '10.1007/s00737-015-0531-2', '10.1103/RevModPhys.88.021003', 'https://doi.org/10.1101/167171', 'https://doi.org/10.1016/j.chb.2017.04.047', '10.1016/j.trb.2016.09.005', '10.1016/j.ancene.2016.01.001', '10.1111/adb.12322', '10.1017/njg.2016.45', '10.1080/1359432X.2016.1209489', '10.1117/1.JBO.21.6.066008', '10.5194/gmd-10-3329-2017', '10.1016/j.rser.2017.01.103', '10.1177/2050157916664559', '10.1007/978-3-319-45931-8_17', '10.1007/s11136-015-1171-8', '10.1145/2991079.2991121', '10.1093/cz/zow089', '10.1126/science.aac8167', '10.1007/s00586-016-4606-1', '10.1186/s12937-017-0229-6', '10.1007/s11357-016-9894-1', '10.1080/00130095.2015.1094371', '10.1016/j.epsl.2016.02.028', '10.1371/journal.pone.0168636', '10.1016/j.atmosres.2016.03.016', '10.1111/deci.12206', '10.1126/science.aad9634', '10.1103/PhysRevA.94.012506', '10.4103/0019-5545.196846', '10.1016/j.cedpsych.2017.01.006', '10.3324/haematol.2015.133470', '10.1057/978-1-137-50956-7', '10.1016/j.scico.2016.04.001', 'https://doi.org/10.1016/j.scico.2016.04.001', '10.1080/03081087.2015.1053425', '10.3758/s13423-017-1270-3', '10.1681/ASN.2015030287', '10.1016/j.avb.2016.05.006', '10.1177/0971333616689191', '10.1002/sej.1243', '10.1016/j.foreco.2017.06.023', '10.1103/PhysRevLett.118.071801', 'https://doi.org/10.1093/geront/gnv127', '10.1007/978-3-319-42324-1_16', '10.1109/JBHI.2015.2412656', '10.1016/j.jeem.2016.04.002', '10.1080/00207543.2015.1058982', '10.1038/mp.2016.100', '10.1080/03003930.2016.1194267', '10.1016/j.envint.2017.01.018', '10.1038/pr.2015.179', '10.1177/1753193416669263', '10.1016/j.tre.2016.11.003', '10.1021/acs.jpcc.5b12016', '10.1002/anie.201603510', '10.1073/pnas.1607005113', '(DOI) - 10.1111/cch.12521', '10.1017/S0016756815000886', '10.1080/1350293X.2015.1073507', '10.1152/jn.00701.2015', '10.1371/journal.pone.0170791', '10.1016/j.seares.2016.07.005', '10.1016/j.reseneeco.2016.03.003', '10.1007/s00531-017-1499-0', '10.1007/s41669-017-0014-7', '10.1093/acrefore/9780190228613.013.439', '10.14814/phy2.13201', '10.1016/j.jtrangeo.2016.10.013', '10.1523/JNEUROSCI.3658-16.2017', '10.1192/bjpo.bp.115.000166', '10.1136/bmjgh-2016-000109', '10.7554/eLife.20320.001', '10.1037/pas0000332', '10.1177/1474704916673841', '10.1057/978-1-137-58179-2', '10.1002/ejp.963', '10.1017/thg.2016.78', '10.1038/tpj.2016.32', '10.1016/j.jesp.2017.03.008', '10.1287/trsc.2015.0647', '10.1186/s13015-016-0087-3', '10.1016/j.neuroimage.2016.10.030', '10.1371/journal.pone.0169109', '10.1007/s11367-017-1358-z', '10.1080/1369183X.2015.1061425', '10.2196/mental.4614', '10.1002/arp.1564', '10.1021/acs.orglett.6b01023', '10.3847/1538-4357/aa6c47', 'http://www.socialevraagstukken.nl/veiligheid-creeer-je-met-geborgenheid/', '10.1186/s12888-016-0790-0', '10.1371/journal.pone.0155755', '10.1103/PhysRevLett.116.241801']
