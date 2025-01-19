#include <iostream>

/* GUI-2376 [No fix this issue] GUI-2376 Should show ... when long name at bridge name */

int main() {
  std::string tooltipText = "<b>List:</b><br><b>h1/p1</b><br><b>h1/p2</b><br><b>h1/p3</b><br><b>h1/p4</b><br><b>h1/p5</b><br>";
  std::string textStart = "<b>";
  std::string textBreak = "<br>";
  std::string textEnd = "</b>";
  auto lengthText = tooltipText.length();
  std::cout << "Length text: " << lengthText << '\n';
  size_t startPos = 0;
  std::cout << "Init start pos: " << startPos << '\n';
  auto endPos = tooltipText.find(textEnd, startPos);
  std::cout << "Init end pos: " << endPos << '\n';
  std::cout << "##################################################\n";
  while(startPos < lengthText) {
    std::string subText = tooltipText.substr(startPos + textStart.length(), endPos - startPos - textStart.length());
    std::cout << subText << '\n';
    std::cout << "##################################################\n";
    std::string replaceText = "XYZ";
    tooltipText.replace(startPos + textStart.length(), endPos - startPos - textStart.length(), replaceText);
    std::cout << tooltipText << '\n';
    std::cout << "##################################################\n";
    startPos += textStart.length() + replaceText.length() + textEnd.length() + textBreak.length();
    std::cout << "Start pos: " << startPos << '\n';
    endPos = tooltipText.find(textEnd, startPos);
    if (endPos > lengthText) break;
    std::cout << "End pos: " << endPos << '\n';
  }
  return 0;
}