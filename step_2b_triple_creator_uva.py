# This file is formatted without line wrapping. Turn LINE WRAPPING OFF for optimal viewing.


## TODO: Re-write rdfCreator.py as an object oriented module
## TODO: Use different domain names and prefixes for ontology, instances ,datasets, etc...
## TODO: Add basic class equivalencies (e.g., article = JournalArticle) to script
## TODO: Link rdfCreator output to existing URIs on VU research portal, etc

#Parameters
from step_1b_parser_uva import vu_bibliography
source_bibliography = vu_bibliography
origin_bibliography = 'uva'


from triplicator.rdfCreator import *
from preprocessor.string_tools import String
from preprocessor.Text_File import Log_File
from meta.consoleOutput import ConsoleOutput

# for logging
console = ConsoleOutput()
log_file = Log_File('log.txt')
current_progress = 0
maximum_progress = len(source_bibliography.entries.items())

#################################################################################
#                   STATIC DEFINITIONS: PROPERTIES, CLASSES                     #
#################################################################################

# Legend:
# c_ = class
# p_ = property
# i_ = instance
# b_ = Bibliography class object field/value


###### NAMESPACE PREFIX DEFINITIONS ######
ont  = "http://clokman.com/kfir/ontology#"  # assign long domain  name to short variable.
res  = "http://clokman.com/kfir/resource#"  # assign long domain  name to short variable.
rdf  = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
rdfs = "http://www.w3.org/2000/01/rdf-schema#"
owl  = "http://www.w3.org/2002/07/owl#"
xsd  = "http://www.w3.org/2001/XMLSchema#"

#add_prefix_triple("",    ont)
#add_prefix_triple("res",  res)
#add_prefix_triple("rdf",  rdf)
#add_prefix_triple("rdfs", rdfs)
#add_prefix_triple("owl",  owl)
#add_prefix_triple("xsd",  xsd)


###### ONTOLOGY DEFINITIONS ######
#add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "http://www.w3.org/2002/07/owl#Ontology")
#add_triple("<http://clokman.com/ontologies/pure-vu>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "http://www.w3.org/2002/07/owl#Ontology")

###### A REQUIRED CLASS DEFINITION FOR PROPERTIES ######
# Although class definitions and assertions will come later, this one is needed for property definitions.
# ... so it is placed here as an exception.
c_object_property  = construct_uri(owl,  "ObjectProperty"    )


###### STATIC PROPERTY DEFINITIONS (p_) ######
p_subclass_of             = construct_uri(rdfs, "subClassOf"        )  # assign URI to subclass of
p_is_author_of            = construct_uri(ont,  "isAuthorOf"        )  # assign URI to is author of
p_has_author              = construct_uri(ont,  "hasAuthor"         )  # ...
p_is_published_on         = construct_uri(ont,  "isPublishedOn"     )
p_is_published_by         = construct_uri(ont,  "isPublishedBy"     )
p_is_published_on_year    = construct_uri(ont,  "isPublishedOnYear" )
p_is_published_on_month   = construct_uri(ont,  "isPublishedOnMonth")
p_is_published_on_date    = construct_uri(ont,  "isPublishedOnDate" )
p_has_doi                 = construct_uri(ont,  "hasDOI"            )
p_has_issn                = construct_uri(ont,  "hasISSN"           )
p_has_isbn                = construct_uri(ont,  "hasISBN"           )
p_is_chapter_of           = construct_uri(ont,  "isChapterOf"       )
p_has_topic               = construct_uri(ont,  "hasTopic")
p_has_abstract            = construct_uri(ont,  "hasAbstract"           )
p_has_origin_bibliography = construct_uri(ont,  "hasOriginBibliography")
p_rdf_type                = construct_uri(rdf,  "type"              )
p_label                   = construct_uri(rdfs, "label"             )
p_equivalent_class        = construct_uri(owl,  "equivalentClass"   )

add_triple(p_subclass_of,              p_rdf_type,     c_object_property)
add_triple(p_is_author_of,             p_rdf_type,     c_object_property)  # x (e.g., p_is_author_of) is a property
add_triple(p_has_author,               p_rdf_type,     c_object_property)
add_triple(p_is_published_on,          p_rdf_type,     c_object_property)
add_triple(p_is_published_by,          p_rdf_type,     c_object_property)
add_triple(p_is_published_on_year,     p_rdf_type,     c_object_property)
add_triple(p_is_published_on_month,    p_rdf_type,     c_object_property)
add_triple(p_is_published_on_date,     p_rdf_type,     c_object_property)
add_triple(p_has_doi,                  p_rdf_type,     c_object_property)
add_triple(p_has_issn,                 p_rdf_type,     c_object_property)
add_triple(p_has_isbn,                 p_rdf_type,     c_object_property)
add_triple(p_is_chapter_of,            p_rdf_type,     c_object_property)
add_triple(p_rdf_type,                 p_rdf_type,     c_object_property)
add_triple(p_label,                    p_rdf_type,     c_object_property)
add_triple(p_has_topic,                p_rdf_type,     c_object_property)
add_triple(p_has_abstract,             p_rdf_type,     c_object_property)
add_triple(p_equivalent_class,         p_rdf_type,     c_object_property)
add_triple(p_has_origin_bibliography,  p_rdf_type,     c_object_property)


#################################################################################
#       DOCUMENT CLASS DECLARATIONS AND CLASS EQUIVALENCY ASSERTIONS            #
#################################################################################

###### STATIC CLASS DEFINITIONS (c_ )######
c_document         = construct_uri(ont,  "Document"          )  # assign URI to document superclass
c_journal          = construct_uri(ont,  "Journal"           )  # assign URI to Journal class
c_topic            = construct_uri(ont,  "Topic"             )
c_named_individual = construct_uri(owl,  "NamedIndividual"   )
#'c_object_property' is not defined here as is in other similar cases, but is defined previously,
# before property definitions and assertions, as it is needed by them.
c_class            = construct_uri(rdfs, "Class"             )
c_bibliography     = construct_uri(res,  "Bibliography")
c_vu_pure          = construct_uri(res,  "VUPure")
c_uva_pure         = construct_uri(res,  "UVAPure")
c_oc               = construct_uri(res,  "OpenCitations")

# Select origin bibliography based on keyword parameter
if origin_bibliography == 'vu':
    current_origin_bibliography = c_vu_pure
elif origin_bibliography == 'uva':
    current_origin_bibliography = c_uva_pure
elif origin_bibliography == 'oc':
    current_origin_bibliography = c_oc
else:
    raise ValueError('Keyword argument "%s" for parameter "origin_bibliography" is unknown.' % origin_bibliography)


# TODO: TRY TO ADD THESE AND SEE WHAT HAPPENS IN PROTEGE:
# add_triple(c_document, p_rdf_type, c_class)
# add_triple(c_journal, p_rdf_type, c_class)
add_triple(c_topic, p_rdf_type, c_class)
# add_triple(c_named_individual, p_rdf_type, c_class)
# add_triple(c_object_property, p_rdf_type, c_class)
# add_triple(c_class, p_rdf_type, c_class)

# Bibliography origin class definitions
add_triple(c_vu_pure,  p_rdf_type, c_class)
add_triple(c_uva_pure, p_rdf_type, c_class)
add_triple(c_oc,       p_rdf_type, c_class)

add_triple(c_vu_pure,  p_subclass_of, c_bibliography)
add_triple(c_uva_pure, p_subclass_of, c_bibliography)
add_triple(c_oc,       p_subclass_of, c_bibliography)

# SR document type definitions
# These are not used to categorize instances in the document directly, but necessary for the class equivalencies with
# Pure-VU document types. As these are the document classes in the main ontology, their variable names are not suffixed
# as in other cases (e.g., c_article_res).
c_journal_article = construct_uri(ont, "JournalArticle")
c_book            = construct_uri(ont, "Book")
c_book_chapter    = construct_uri(ont, "BookChapter")
c_miscellaneous   = construct_uri(ont, "Miscellaneous")

add_triple(c_journal_article,  p_rdf_type, c_class)
add_triple(c_book,             p_rdf_type, c_class)
add_triple(c_book_chapter,     p_rdf_type, c_class)
add_triple(c_miscellaneous,    p_rdf_type, c_class)

############################################################################################################
# SECTION COMMENTED OUT (ON 14th OF FEB) TO PREVENT DUPLICATE CLASSES SUCH AS 'BOOK'(ont) and 'BOOK'(vu)
# IF LEADS TO A PROBLEM WITH SR ONTOLOGY, IT SHOULD BE TURNED BACK ON OR ADAPTED IN A DIFFERENT WAY
# # Pure-VU document type definitions
# # These are necessary for class equivalency assertions between Pure-VU and SR document classes
# # These pure VU class names (e.g., 'article', 'book', 'inbook') are not coded anywhere in these scripts, but they are parsed with the below names by pybtex package.
# # These classes are *automatically* (hence no explicit usage anywhere) used to assign types to instances in the code below.
# # As these are NOT the document classes in the main ontology, their variable names are suffixed (e.g., c_article_res).
# c_article_res = construct_uri(res, "article")
# c_book_res    = construct_uri(res, "book")
# c_inbook_res  = construct_uri(res, "inbook")
# c_misc_res    = construct_uri(res, "misc")
#
# add_triple(c_article_res,    p_rdf_type, c_class)
# add_triple(c_book_res,       p_rdf_type, c_class)
# add_triple(c_inbook_res,     p_rdf_type, c_class)
# add_triple(c_misc_res,       p_rdf_type, c_class)
#
#
# # Class equivalency assertions
# add_triple(c_article_res, p_equivalent_class, c_journal_article)
# add_triple(c_book_res,    p_equivalent_class, c_book)
# add_triple(c_inbook_res,  p_equivalent_class, c_book_chapter)
# add_triple(c_misc_res,    p_equivalent_class, c_miscellaneous)
############################################################################################################

#################################################################################
#                     DYNAMIC TRIPLES: INSTANCES AND TYPES                      #
#################################################################################

for each_entry_id, each_entry in source_bibliography.entries.items():

    #TODO: this try-except block is a workaround [001]. remove it.
    try:
        #######  URIs  #######
        current_document_instance_name = each_entry["b_document"]  # document instance
        current_type = each_entry["b_type"]  # type
        current_type = String(current_type).capitalize_first_letter().content

    except:
        pass
    # NOTE: Do not move the lines below to category and instance definitions section in the beginning of the script. c_document_type values need to be dynamically assigned within this for loop, as the document classes (e.g., Article, Book) are extracted from the resource file.

    c_document_type      = construct_uri(ont, current_type                  )  # extract the class of the current document (e.g., Article, Book) and assign it to the current iteration of the c_document_type variable
    i_document_instance   = construct_uri(res, current_document_instance_name)  # assign current document instance to an instance variable (denoted by i_), and give it an URI


    #######  DOCUMENT INSTANCE + DOCUMENT TYPE + DOCUMENT #######
    add_triple(i_document_instance,  p_rdf_type,       c_named_individual)  # the current document is an an instance
    add_triple(c_document_type,      p_subclass_of,    c_document        )  # make current document's class a subclass of the superclass "Document".
    add_triple(i_document_instance,  p_rdf_type,       c_document_type   )  # bind the extracted document classes to the document instances (the latter was extracted previously in this loop)
    add_triple(i_document_instance,  p_rdf_type,       c_document        )  # make current document an instance of class "Document".


    ########  DOCUMENT ORIGIN BIBLIOGRAPHY  #######
    add_triple(i_document_instance,  p_has_origin_bibliography,  current_origin_bibliography)  # the document comes from the given bibliography


    #######  DOCUMENT LABEL  #######
    #TODO: this try-except block is a workaround. remove it.
    try:
        add_triple(i_document_instance, p_label, construct_string_literal(each_entry["b_document_label"], "@en"))
    except:
        pass

    #######  AUTHOR  ########
    #TODO: this try-except block is a workaround. remove it.
    try:
        current_authors                = each_entry["b_authors"]                 # authors
        current_author_labels          = each_entry["b_author_labels"]
    except:
        pass

    for each_current_author, each_current_author_label in zip(current_authors, current_author_labels):

        # Assign author to instance
        i_author = construct_uri(res, each_current_author)  # assign this author to an instance variable (denoted by i_), and give it an URI

        # Bind the instances to each other and define their types
        add_triple(i_author,             p_is_author_of,    i_document_instance)  # the current author is the author of the current document
        add_triple(i_document_instance,  p_has_author,      i_author)
        add_triple(i_author,             p_rdf_type,        c_named_individual)   # the current author is an an instance

        # Add author label
        add_triple(i_author,      p_label,            construct_string_literal(each_current_author_label, "@en"))


    #######  PUBLICATION INSTANCE + PUBLISHED ON  #######
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    # This property applies journal articles (but not to books and journals)
    try:
        current_journal = each_entry["b_journal"]         # extract current publication instance
        i_journal       = construct_uri(res, current_journal)  # create  URI from publication instance

        # Bind the instances to each other and define their types
        add_triple(i_document_instance,   p_is_published_on,  i_journal         )  # the current document is published on the current publication
        add_triple(i_journal,             p_rdf_type,         c_named_individual)  # the current publication is an instance

    except:
        pass


    #######  PUBLISHER  #######
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    # This property applies to books and journals (but not to journal articles)
    try:
        current_publisher = each_entry["b_publisher"]          # extract current publisher instance
        i_publisher       = construct_uri(res, current_publisher)  # create  URI from publisher instance

        # Bind the instances to each other and define their types
        add_triple(i_document_instance,   p_is_published_by,  i_publisher         )  # the current document is published by the current publisher
        add_triple(i_publisher,           p_rdf_type,         c_named_individual)    # the current publisher is an instance

    except:
        pass


    #######  YEAR + MONTH + DATE #######
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    try:
        current_year  = each_entry["b_publication_year"]    # extract current publication year
        current_month = each_entry["b_publication_month"]   # extract current publication month
        current_date  = current_year + "." + current_month      # extract current publication combine them into a date

        # Bind the instances to each other and define their types
        # NOTE: Literals are constructed as strings instead of integers due to LD-R compatibility issues.
        # (LD-R had trouble querying years if they were integers.)
        # If these string years need to be turned into integers in future, though, use 'construct_integer_literal()'.
        add_triple(i_document_instance,   p_is_published_on_year,  construct_string_literal(current_year))    # the current document is published on the current year
        add_triple(i_document_instance,   p_is_published_on_month, construct_string_literal(current_month))   # the current document is published on the current month
        add_triple(i_document_instance,   p_is_published_on_date,  construct_string_literal(current_date))    # the current document is published by the current date

    except:
        try: # In case "month" is missing, just process "year".
            current_year = each_entry["b_publication_year"]  # extract current publication year
            add_triple(i_document_instance,   p_is_published_on_year,  construct_string_literal(current_year)) # the current document is published by the current publisher

        except: # In case there is neither year or month
            pass


    #######  DOI  #######
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    try:

        # Extract current doi
        current_doi = each_entry["b_doi"]

        # Bind the values to instances, and define their types
        add_triple(i_document_instance,   p_has_doi,   construct_string_literal(current_doi))   # the current document is published by the current publisher

    except:
        pass


    #######  ISSN  #######
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    try:
        # Extract current issn
        current_issn = each_entry["b_issn"]

        # Bind the values to instances, and define their types
        add_triple(i_document_instance,   p_has_issn,  construct_string_literal(current_issn))  # the current document is published by the current publisher

    except:
        pass


    #######  ISBN  #######
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    try:
        # Extract current isbn
        current_isbn = each_entry["b_isbn"]

        # Bind the values to instances, and define their types
        add_triple(i_document_instance,   p_has_isbn,  construct_string_literal(current_isbn))  # the current document is published by the current publisher

    except:
        pass


    #######  BOOK TITLE --> IS CHAPTER IN + PARENT BOOK INSTANCE #######
    # Assign parent book to the current document if available (i.e., if the current document is a book chapter).
    # Also infer parent book instance.
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    try:
        # Extract current book title
        current_parent_book = each_entry["b_parent_book"]

        # Bind the values to instances, and define their types
        i_current_parent_book = construct_uri(res, current_parent_book)

        add_triple(i_document_instance,   p_is_chapter_of,  i_current_parent_book)  # the current document is published by the current publisher
        add_triple(i_current_parent_book, p_rdf_type,       c_book)

    except:
        pass


    #######  KEYWORDS --> ABOUT  #######
    # Assign keywords to the current document if available and the keyword is not in ignore list.
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    try:
        current_topics           = each_entry["b_topics"]
        list_of_topics_to_ignore = ["Journal_Article", "journal_article"]  # ignore these topics
        for each_topic in current_topics:
            if each_topic not in list_of_topics_to_ignore:  # if the topic is not in the ignore list...
                # Construct current topic uri dynamically for each topic
                c_current_topic = construct_uri(res, each_topic)

                # Connect document instance to each of these topics
                add_triple(i_document_instance, p_has_topic, c_current_topic)

                # And clarify that the 'current topic' is a subclass of 'topic'
                add_triple(c_current_topic, p_subclass_of, c_topic)
    except:
        pass


    #######  ABSTRACT  #######
    # Assign abstract to the current document if available and the keyword is not in ignore list.
    # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields except these ones may not always be present.
    try:
        current_abstract = each_entry["b_abstract"]
        list_of_values_to_ignore = []  # ignore these values if they are found in the abstract field

        if current_abstract not in list_of_values_to_ignore:  # if the abstract is not in the ignore list...
            # Construct string literal for current abstract dynamically for each abstract
            c_current_abstract = construct_string_literal(current_abstract, '@en')

            # Connect document instance to each of the abstracts
            add_triple(i_document_instance, p_has_abstract, c_current_abstract)
    except:
        pass


    # Progress bar update
    console.print_current_progress(current_progress, maximum_progress, 'Converting Bibliography object to .ttl file')
    current_progress += 1

# from pprint import pprint
#pprint(triples_list)  # 'triples list' variable resides in rdfCreator.py