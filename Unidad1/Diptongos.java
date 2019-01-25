
import java.io.File; 
import java.io.FileNotFoundException;
import java.util.Scanner; 
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Héctor Rodríguez
 */
public class Diptongos {

    public static void main(String[] args) {   
        String vocales = "aeiou";
        
        File file = new File("parrafo.txt"); 
        Scanner sc = null; 
        
        try {
            sc = new Scanner(file);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Diptongos.class.getName()).log(Level.SEVERE, null, ex);
        }

        int lineNumber = 1;
        
        while (sc.hasNextLine()) {
            String[] palabras = sc.nextLine().split(" ");
            for(String palabra : palabras){
                char vocalAntes = ' ';
                for(char letra : palabra.toCharArray()) {
                    if (vocales.contains(String.valueOf(letra))) {
                        if ((vocalAntes != ' ') && (vocalAntes != letra)) {
                            System.out.println("\nPalabra: " + palabra);
                            System.out.println("Diptongo: " + vocalAntes + letra);
                            System.out.println("En la linea: " + lineNumber);
                        }
                        vocalAntes = letra;
                    } else {
                        vocalAntes = ' ';
                    }
                }
            }
            lineNumber++;
        }
    }
    
}