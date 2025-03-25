<script>
  import { Router, Route } from "svelte-routing";

  import Login from "./login.svelte";
  import Calendar from "./calendar.svelte";
</script>

<Router>
  <Route path="/">
    <Login></Login>
  </Route>
  <Route path="/calendar">
    <Calendar></Calendar>
  </Route>
</Router>
