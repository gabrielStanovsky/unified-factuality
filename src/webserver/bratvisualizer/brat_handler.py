import json
import networkx as nx
from cgi import escape
import logging
logging.basicConfig(level = logging.DEBUG)


class Brat:
    """
    Collections of brat handlers
    """

    @staticmethod
    def sent_to_html(sent, annots):
        """
        Returns the html format represenation
        """
        split_sent = sent.split(' ')
        entities = ",\n".join(["['A{0}_{1}', '{2}', [[{0}, {1}]]]".format(char_start, char_end, fact_val)
                               for ((char_start, char_end), fact_val) in
                               [(Brat.word_to_char(split_sent, (n, n + 1)),
                                      str(val)) for (n, val) in annots.iteritems()]])

        brat_input = [(entities, '')]
        return Brat.get_brat_html(sent, brat_input)

    @staticmethod
    def output_brat_html(sent, annots, filename):
        """
        Visualize the give digraph (networkx object) using brat
        output to the given fileaname.
        @param sent:  Space separated string
        @param digraph: Netowrkx object
        @param filename: file name in which to write the html code
        """
        html = sent_to_html(sent, annots)

        with open(filename, 'w') as fout:
            fout.write(html)

        logging.debug("output written to: {}".format(filename))

    @staticmethod
    def word_to_char(sent, (word_start, word_end)):
        """
        Given a tuple node indicating word start and end indices,
        return its corresponding char indices
        """
        word_end = word_end -1
        return (word_start + sum(map(len, sent[: word_start])),
                word_end + sum(map(len, sent[: word_end])) + len(sent[word_end]))

    @staticmethod
    def get_brat_name(node):
        """
        Get brat name for a given node
        """
        return "A{}_{}".format(*node)


    @staticmethod
    def get_brat_html(sent, graphs):
        """
        Return a brat html text of graphs (list of entities and relations
        sent is a string representing the sentence
        """
        docdata = "\n".join([Brat.brat_template.replace("SENTENCE_STUB",
                                                        sent).\
                             replace("ENTITIES_STUB",
                                     entities).\
                             replace("RELATIONS_STUB",
                                     rels).\
                             replace("LABEL_NUM_STUB",
                                     str(graph_ind))
                             for graph_ind, (entities, rels) in enumerate(graphs)])

        embedding = "\n".join([Brat.embedding_template.replace("LABEL_NUM_STUB", str(i))
                               for i in range(len(graphs))])

        div = "\n".join([Brat.div_template.replace("LABEL_NUM_STUB", str(i))
                               for i in range(len(graphs))])


        return Brat.html_template.replace("DOCDATA_STUB", docdata).\
            replace("EMBEDDING_STUB", embedding).\
            replace("DIV_STUB", div)


    brat_template = """
    var docData_LABEL_NUM_STUB = { text: "SENTENCE_STUB",

    entities: [

    ENTITIES_STUB

    ],

    relations: [

    RELATIONS_STUB

    ]
    };

    """

    embedding_template = """
        Util.embed(
        // id of the div element where brat should embed the visualisations
        'label_LABEL_NUM_STUB',
        // object containing collection data
        collData,
        // object containing document data
        docData_LABEL_NUM_STUB,
        // Array containing locations of the visualisation fonts
        webFontURLs
        );
    """

    div_template = """
    <div id="label_LABEL_NUM_STUB"></div>
    <br><br>
    """

    html_template = """
    <html>
 <head>
   <link rel="stylesheet" type="text/css" href="http://u.cs.biu.ac.il/~stanovg/brat/style-vis.css"/>
   <script type="text/javascript" src="http://u.cs.biu.ac.il/~stanovg/brat/client/lib/head.load.min.js"></script>
</head>
<body>


    <script language="javascript">

    var bratLocation = 'http://u.cs.biu.ac.il/~stanovg/brat';
head.js(
    // External libraries
    bratLocation + '/client/lib/jquery.min.js',
    bratLocation + '/client/lib/jquery.svg.min.js',
    bratLocation + '/client/lib/jquery.svgdom.min.js',

    // brat helper modules
    bratLocation + '/client/src/configuration.js',
    bratLocation + '/client/src/util.js',
    bratLocation + '/client/src/annotation_log.js',
    bratLocation + '/client/lib/webfont.js',

    // brat modules
    bratLocation + '/client/src/dispatcher.js',
    bratLocation + '/client/src/url_monitor.js',
    bratLocation + '/client/src/visualizer.js'
    );

    var webFontURLs = [
    bratLocation + '/static/fonts/Astloch-Bold.ttf',
    bratLocation + '/static/fonts/PT_Sans-Caption-Web-Regular.ttf',
    bratLocation + '/static/fonts/Liberation_Sans-Regular.ttf'
    ];


    var collData = {

    entity_types: [ {
            type   : 'Predicate',
            labels : ['Predicate', 'Pr'],
            bgColor: '#7fa2ff',
            borderColor: 'darken'
    },
    {
            type   : 'Argument',
            labels : ['Argument', 'Ar'],
            bgColor: '#ff6a36',
            borderColor: 'darken'
    },
]
    };




    DOCDATA_STUB


     head.ready(function() {
    EMBEDDING_STUB

});

  </script>

    DIV_STUB


</body>
</html>
"""
