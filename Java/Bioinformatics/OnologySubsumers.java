import org.apache.log4j.Level;
import org.apache.log4j.LogManager;
import org.semanticweb.elk.owlapi.ElkReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.*;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * Program to find all superclasses of given axioms in an ontology using the
 * Elk Reasoner (https://github.com/liveontologies/elk-reasoner)
 * and write them to a tab-separated file.  Makes heavy use of example file
 * from the OWL API for Java (https://github.com/owlcs/owlapi)
 *
 * For CSC 526-01: Bioinformatics, Spring 2019, Dr. Prashanti Manda, UNCG
 *
 * @author James Knox Polk <jkpolk@uncg.edu>
 *
 * Last updated 02/06/2019
 */
class Assignment1 {

    private static final String owlFile = "go.owl";

    public static void main(String[] args) {

        String [] goArray = new String[]{
                "GO_0003677",
                "GO_0003700",
                "GO_0005634",
                "GO_0006355",
                "GO_0006986",
                "GO_0016020",
                "GO_0016021",
                "GO_0043565",
                "GO_0045449",
                "GO_0046983"
        };

        GOowl goowl = new GOowl(owlFile, goArray);

        goowl.setOwlFile(owlFile);
        goowl.setGoArray(goArray);

        goowl.loadOntology();
    }


}
class GOowl {
    private static final String FILEPATH = "CSC 526-01_Assignment 1_JPolk.tsv";
    private String owlFile;
    private String [] goArray;

    GOowl(String owlFile, String[] goArray) {
        this.owlFile = owlFile;
        this.goArray = goArray;
    }

    void loadOntology(){
        // Get hold of an ontology manager
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        File file = new File(getOwlFile());
        // Now load the local copy
        OWLOntology localGO = null;
        try {
            localGO = manager.loadOntologyFromOntologyDocument(file);
        } catch (OWLOntologyCreationException e) {
            e.printStackTrace();
        }
        System.out.println("Loaded ontology: " + localGO);
        // We can always obtain the location where an ontology was loaded from
        IRI documentIRI = manager.getOntologyDocumentIRI(localGO);
        System.out.println("    from: " + documentIRI);

        createReasoner(localGO, manager);
    }

    private void createReasoner(OWLOntology owlOntology, OWLOntologyManager manager) {

        // We need to create an instance of OWLReasoner. An OWLReasoner provides
        // the basic query functionality that we need, for example the ability
        // obtain the subclasses of a class etc. To do this we use a reasoner
        // factory. Create a reasoner factory. In this case, we will use ELK
        // (https://github.com/liveontologies/elk-reasoner/wiki/ElkOwlApi)
        LogManager.getLogger("org.semanticweb.elk").setLevel(Level.OFF);
        OWLReasonerFactory reasonerFactory = new ElkReasonerFactory();
        OWLReasonerConfiguration config = new SimpleConfiguration();
        // Create a reasoner that will reason over our ontology and its imports
        // closure. Pass in the configuration.
        OWLReasoner reasoner = reasonerFactory.createReasoner(owlOntology, config);
        // Ask the reasoner to do all the necessary work now
        reasoner.precomputeInferences();
        // We can determine if the ontology is actually consistent (in this
        // case, it should be).
        boolean consistent = reasoner.isConsistent();
        if (consistent)
            System.out.println("Ontology is consistent. Continuing...");
        else
            System.out.println("WARNING: Ontology is NOT consistent");
        System.out.println("\n");


        List<String> superclassList = new ArrayList<>();
        String baseClass;

        for (String s : goArray) {

            //System.out.println("Superclasses of " + s + ": ");
            baseClass = new StringBuilder().append(s).append("\t").append(printSuperClasses(s, manager, reasoner)).toString();
            superclassList.add(baseClass);
        }

        bufferedWrite(superclassList);

    }

    private String printSuperClasses (String id, OWLOntologyManager manager, OWLReasoner reasoner) {
        StringBuilder superClassesOfBase = new StringBuilder();
        // Now we want to query the reasoner
        OWLDataFactory fac = manager.getOWLDataFactory();

        // Get a reference to the GO class so that we can as the
        // reasoner about it. The full IRI of this class happens to be:
        // <http://owl.man.ac.uk/2005/07/sssw/people#vegetarian>
        OWLClass goClass = fac.getOWLClass(IRI
                .create("http://purl.obolibrary.org/obo/"+id+""));

        // Get the set of named classes that are the strict (potentially direct)
        // super classes of the specified class expression with respect
        // to the imports closure of the root ontology.
        NodeSet<OWLClass> superClasses = reasoner.getSuperClasses(goClass, false);

        // The reasoner returns a NodeSet, which represents a set of Nodes.
        // In this case, we don't particularly care about
        // the equivalences, so we will flatten this set of sets and print the
        // result
        Set<OWLClass> clses = superClasses.getFlattened();


        // Trim the class name to just the GO number and format the output.
        for (OWLClass cls : clses) {
            if (!cls.toString().equalsIgnoreCase("owl:Thing")) {
                String className = cls.toStringID().substring(31);
                superClassesOfBase.append(className).append(",");
            }
        }

        // Remove last comma and return the string
        superClassesOfBase.setLength(Math.max(superClassesOfBase.length() - 1, 0));
        return superClassesOfBase.toString();
    }
    private static void bufferedWrite(List<String> content) {

        Path fileP = Paths.get(GOowl.FILEPATH);
        Charset charset = Charset.forName("utf-8");

        try (BufferedWriter writer = Files.newBufferedWriter(fileP, charset)) {
            System.out.println("Opening file " + fileP + " for writing.");
            for (String line : content) {
                writer.write(line, 0, line.length());
                writer.newLine();
            }
            System.out.println("Write finished. Closing file " + fileP + ".");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String getOwlFile() {
        return owlFile;
    }

    void setOwlFile(String owlFile) {
        this.owlFile = owlFile;
    }

    void setGoArray(String[] goArray) {
        this.goArray = goArray;
    }
}