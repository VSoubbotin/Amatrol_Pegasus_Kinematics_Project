PrintWriter output;
public void settings() {
  size(1000, 1000);
}

String Filename = "VintageAutomobile.svg";
String OutputFile = "positions.txt";
void setup(){
  String[] paths = new String[0];
  String[] lines = loadStrings(Filename);
  for (int i = 0 ; i < lines.length; i++) {
    String[] split = split(lines[i], '"');
    for  (int n = 0 ; n < split.length; n++) {
      String temp = split[n];
      if (temp.length() > 4) {
        if ((temp.substring(0, 4)).equals("path")) {
          paths = append(paths, temp);
          println(temp);
        }
      }
    }
  }
  output = createWriter(OutputFile);
  PShape map = loadShape(Filename);
  println(paths.length);
  for (int i = 0 ; i < paths.length; i++) {
    //size((int)map.width,(int)map.height);
    //fetch the border shape - peaked at the path name using Illustrator
    PShape border = map.getChild(paths[i]);
    //manually traverse the path
    for(int n = 0 ; n < border.getVertexCount(); n++){
    //vertex(border.getVertexX(i),border.getVertexY(i));
      output.println(str(border.getVertexX(n)) + " " + str(border.getVertexY(n)));
    }
    output.println("end");
  }
  output.flush(); // Writes the remaining data to the file
  output.close(); // Finishes the file
}
