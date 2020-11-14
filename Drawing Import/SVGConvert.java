public class PShape
extends java.lang.Object
implements PConstants;
Pshape map;
// package processing.core;
// import processing.core.PApplet;
// public class PShape implements PConstants {
//   protected String name;
//   protected Map<String,PShape> nameTable;
// public void setup(){
  
// }

  public static void main(String []args) {
    PShape map = loadShape("Afghanistan_location_map.svg");
  size((int)map.width,(int)map.height);
  //fetch the border shape - peaked at the path name using Illustrator
  PShape border = map.getChild("path157");
  //manually traverse the path
  beginShape();
  for(int i = 0 ; i < border.getVertexCount(); i++){
    vertex(border.getVertexX(i),border.getVertexY(i));
  }
  endShape();
  }
