# simple-FJE
A simple tool to visualize JSON file in terminal. Supporting two style( tree &amp; rectangle) and 5 icon family( card &amp; king &amp; simple & heart &amp; weather). 

Easy to extend the icon family by similarly writing whatever you want in the config.py.  

The format code for running the project is : fje -f <json file> -s <style> -i <icon family>.

for the fje_v2， I introduce iterator & strategy mode in order to provide a function for visit the element sequentially without showing the inner logic which makes the code more flexible.
