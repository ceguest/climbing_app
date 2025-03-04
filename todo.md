Features
* add a way to filter by projects for a person
  * with a project column containing a list of names?
  * would have to have a way of editing routes to add/remove project
  * maybe have an advanced filter in pop out?
* update 47 (Brown Dots) to have correct holds and updated grade
* add different grading for different footholds
* update check route exists, should there be an override for different feet?
  * Should this move into the route adder?

Refactoring
* remove naming clash 'id' throughout route handler etc (existing function)
* add method to update routes
* add method to update holds picture

Bugs
* there is an error being thrown and not caught by something in route adder
  ** this is if a click event happens outside the parameters of the hold location + tolerance i.e. no hold ID returned so can't continue next command with blank parameter **
* handle closing the route menu better, e.g. if you click outside the menu
* handle clicking edit rout better where no route selected

Done
* make routes in listbox have id, name and grade
* create grade filter
* add method to add routes
* add method of adding name, setter etc
* make window size better
* stop add route needing basic layout
* grade listbox needs to update after a new route is added
* add route notes
* BUG - check_route_exists doesn't work if any route has a blank field (holds or specials)
* check for duplicate routes
* footholds
* edit route

