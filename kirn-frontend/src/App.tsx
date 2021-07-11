import './App.css';
import NavigationBar from './Components/NavigationBar/NavigationBar';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomeRoute from './Routes/HomeRoute/HomeRoute';
import JoinCourseRoute from './Routes/JoinCourseRoute/JoinCourseRoute';

function App() {
  require('dotenv').config()
  return (
    <div className="App">
      <NavigationBar />
      <Router>
        <Switch>
          <Route path="/" exact component={HomeRoute} />
          <Route path="/join/:guildId/:courseName" component={JoinCourseRoute} />
        </Switch>
      </Router>
    </div>
  );
}


export default App;
