import java.io.*;
import java.net.*;

public class JavaExample {

   public static void main(String[] args) throws Exception {


      // Make connection
      URL url = new URL("http://localhost:8080/parse");
      URLConnection urlConnection = url.openConnection();
      urlConnection.setDoOutput(true);
      OutputStreamWriter out = new OutputStreamWriter(urlConnection.getOutputStream());

      // Create query string
      String queryString = "tagged_text=" + URLEncoder.encode("an_DT input_NN string_NN ._.", "UTF-8");

      // Write query string to request body
      out.write(queryString);
      out.flush();

      // Read the response -- only AFTER writing the request!
      BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

      String line = null;
      while ((line = in.readLine()) != null)
      {
	 System.out.println(line);
      }
      out.close();
      in.close(); 
   }
}
