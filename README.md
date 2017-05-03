### Running the code

1. Create a virtual environment (`pyvenv env`) in the top folder
2. Activate virtual environment (`. env/bin/activate`)
3. Install dependencies into the environment using pip (`pip install -r requirements.txt`)
4. Run the Django app:
`````
./manage.py runserver
````````

### Workplan & Deliverables
1. Change the "intervention analysis" graph to an interactive parallel coordinates plot **Done**
2. Modify axes so they have meaningful names instead of symbols **I thought this was done, but found some more colloquial names during our demos. There has definitely been progress though**
3. Add the user's control measure information to the first graph ("SIR Curve(s)") **Done**
4. Get rid of the third and fourth graphs and replace with a series of heat maps that show how effective the control measure is, across the user's defined parameter ranges. **This is now the second graph**
5. Update the user input fields so they are sliding bars instead of input fields. Also fix error handing so if a user puts some that isn't valid they are informed in some sort of useful way.  **I believe this is largely fixed. I had sliding bars, and then actually decided they were hard to use, and moved back to text boxes, but adjusted them to be smaller**
6. Add some background information about what the model is, what the parameters are, and how the model works to a separate FAQ page. **I didn't get to this. Developing this content in a thoughtful way is actually quite time consuming. There is a menu that goes to other pages, but the relevant content still needs work**
