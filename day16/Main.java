/* Advent of code day 16


class: 1-3 5-7

1) Read file
2) Get Rules
3) Process tickets
    1) Check for invalid rules
    2) Store invalid ticket fields
4) Sum scanning error rate

Resources
https://www.journaldev.com/709/java-read-file-line-by-line

  //List<String> lines = Arrays.toString(myObj.Input);

*/
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.*;

public class Main{
      private static String[] Input;
      private static ArrayList<int[]> Rules =  new ArrayList<int[]>();

public String[] getInput(String path) {
    try {
        return Files.lines(Path.of(path)).toArray(String[]::new);
    } catch (IOException e) {
        e.printStackTrace();
        return new String[0];
    }
}


public int[] procString(String line) {
  Pattern p = Pattern.compile(".*:.* ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)", Pattern.CASE_INSENSITIVE);

  Matcher m = p.matcher(line);
  boolean matchFound = m.find();
  if(matchFound) {
    System.out.println("Found value: " + m.group() );
    String printGroups = "found val = ";
    int[] groupmatch = new int[4];
    for (int i = 1; i < 5; i++){
    	groupmatch[i-1] = Integer.parseInt(m.group(i));
    };

    System.out.println(printGroups);
    System.out.println("groupmatch = " + Arrays.toString(groupmatch));
    return groupmatch;
  } else {
    System.out.println("Match not found");
    return new int[0];
  }
}
public int[] StrToInt(String[] array) {
  //Pattern p = Pattern.compile("(class|row|seat):.*(\d+)-(\d+)\s+or\s+(\d+)-(\d+)", Pattern.CASE_INSENSITIVE);
  // See here for initialising integer arrays: https://stackoverflow.com/questions/1200621/how-do-i-declare-and-initialize-an-array-in-java
  int[] intArray = new int[4];
  for (int i=0; i< array.length; i++){
    intArray[i] = Integer.parseInt(array[i]);
  }
  return intArray;
}


public boolean isRule(String line) {
  Pattern p = Pattern.compile(".*:.* ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)", Pattern.CASE_INSENSITIVE);
  Matcher m = p.matcher(line);
  boolean matchFound = m.find();
  return matchFound;
}

public boolean isYourTicket(String line) {
  Pattern p = Pattern.compile(".*your.*ticket", Pattern.CASE_INSENSITIVE);
  Matcher m = p.matcher(line);
  boolean matchFound = m.find();
  return matchFound;
}

public boolean isYourNearbyTickets(String line) {
  Pattern p = Pattern.compile(".*nearby.*ticket", Pattern.CASE_INSENSITIVE);
  Matcher m = p.matcher(line);
  boolean matchFound = m.find();
  return matchFound;
}


public boolean isInt(String line) {
  Pattern p = Pattern.compile("^[0-9].*", Pattern.CASE_INSENSITIVE);
  Matcher m = p.matcher(line);
  boolean matchFound = m.find();
  return matchFound;
}


public void setInput(String path){
    this.Input = getInput(path);
}

public boolean checkIsValid(Integer ticket){
boolean isvalid = false;
// loop over Rules
// for looping
// See: https://beginnersbook.com/2013/12/how-to-loop-arraylist-in-java/
  int count = 0;
  while (Rules.size() > count && !isvalid){
	  int[] rule = Rules.get(count);
      isvalid = checkRuleIsValid(ticket, rule[0], rule[1], rule[2], rule[3]);
      count++;
  }
  return isvalid;
}
public boolean checkRuleIsValid(Integer ticket, Integer min1, Integer max1, Integer min2, Integer max2){
  return (min1 <= ticket && ticket <= max1) || (min2 <= ticket && ticket <= max2);
}

public static void main(String[] args) {
  Main myObj = new Main();
  String[] procLine;
  int[] intLine;
  //myObj.lines = myObj.getInput("day16_Main_input.txt");
  //myObj.setInput("day16_test_input.txt");
  myObj.setInput("day16_input.txt");

  boolean is_rule = true;
  boolean is_my_ticket = false;
  boolean is_nearby_ticket = false;
  boolean is_int = false;
  ArrayList<Integer> my_ticket = new ArrayList<>();
  ArrayList<Integer> nearby_tickets = new ArrayList<>();
  ArrayList<Integer> invalid_tickets = new ArrayList<Integer>();

  for (String line: Input){
    is_int = myObj.isInt(line);
    if (!is_int){
    is_rule = myObj.isRule(line);
    is_my_ticket = myObj.isYourTicket(line);
    is_nearby_ticket = myObj.isYourNearbyTickets(line);
    }
    if (is_rule && !is_int){
      System.out.println("is rule: " + line);
      // add a rule
      intLine = myObj.procString(line);
      Rules.add(intLine);
      System.out.println("adding rule" + Arrays.toString(intLine));

      
    } else if (is_my_ticket && is_int){
      String[] values = line.split(",");
      for (int i=0; i< values.length; i++){
        my_ticket.add(Integer.parseInt(values[i]));
      }
        // Append to array
    } else if (is_nearby_ticket && is_int){
      String[] values = line.split(",");
      for (int i=0; i< values.length; i++){
        nearby_tickets.add(Integer.parseInt(values[i]));
      }
    }
  }


  System.out.println("my_ticket: " + Arrays.deepToString(my_ticket.toArray()));
  System.out.println("nearby_tickets " + Arrays.deepToString(nearby_tickets.toArray()));
  System.out.println("Rules =  " + Arrays.deepToString(Rules.toArray()));


  for (int counter=0; counter < nearby_tickets.size(); counter ++) {
    Integer ticket = nearby_tickets.get(counter);
    boolean is_valid = myObj.checkIsValid(ticket);
    if (!is_valid) {
    	invalid_tickets.add(ticket);
        System.out.println("Found invalid ticket = " + ticket);

    }
  }
  System.out.println("Found invalid tickets = "+ Arrays.deepToString(invalid_tickets.toArray()));
  System.out.println("Expected output = 4, 55, 12");
  int scanning_error_rate = 0;
  for (int counter= 0; counter < invalid_tickets.size(); counter++) {
		  scanning_error_rate += invalid_tickets.get(counter);
  }
  System.out.println("Answer: Scanning error rate = " + scanning_error_rate);

}
}
