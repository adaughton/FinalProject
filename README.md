### Running the code
1. Install homebrew
2. Install postgresql (`brew install postresql`)
3. Create a virtual environment (`pyvenv env`) in the top folder
4. Activate virtual environment (`. env/bin/activate`)
5. Install dependencies into the environment using pip (`pip install -r requirements.txt`)
6. Run the Django app:
`````
./manage.py runserver
````````
### Some notes about parameters

1. Initial number susceptible has to be > 2 (range 1000-10,000 is pretty normal)
2. Initial number infected has to be greater than 0
3. Infectiousness period has to be an integer between 1 and 14
4. R0 range has to be greater than 1, but can be a float. Increasingly large ranges cause the server to give out. This is a problem I'm working on. 
5. Control effectiveness must be between 0 and 1. Floats are acceptable. This describes the fraction of the susceptible population that are removed at each time point (so 0.01-0.1 are realistic values)
6. The control start has to be an integer.

These are also described in popovers on each input.

### Workplan & Deliverables
1. Change the "intervention analysis" graph to an interactive parallel coordinates plot **Done**
2. Modify axes so they have meaningful names instead of symbols **I thought this was done, but found some more colloquial names during our demos. There has definitely been progress though**
3. Add the user's control measure information to the first graph ("SIR Curve(s)") **Done**
4. Get rid of the third and fourth graphs and replace with a series of heat maps that show how effective the control measure is, across the user's defined parameter ranges. **This is now the second graph**
5. Update the user input fields so they are sliding bars instead of input fields. Also fix error handing so if a user puts some that isn't valid they are informed in some sort of useful way.  **I believe this is largely fixed. I had sliding bars, and then actually decided they were hard to use, and moved back to text boxes, but adjusted them to be smaller. I also added popovers that describe the fields.**
6. Add some background information about what the model is, what the parameters are, and how the model works to a separate FAQ page. **I didn't get to this. Developing this content in a thoughtful way is actually quite time consuming. There is a menu that goes to other pages, but the relevant content still needs work**
