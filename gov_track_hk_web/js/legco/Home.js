import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import { withStyles } from 'material-ui/styles';
import Menu from './Menu';
import AbsentRank from './AbsentRank';
import Topbar from '../home/Topbar';

const styles = () => ({
  jumbotron: {
    padding: '0.5em',
    backgroundColor: '#AAA',
    backgroundImage: 'url(/static/gov_bg.png)',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    color: '#FFF',
  },
  container: {
  },
  appBar: {
  },
});


class Home extends Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.container}>
        <Topbar />
        <AppBar position="static" className={classes.appBar}>
           <div className={classes.jumbotron}>
             <h1><div>立法會</div></h1>
           </div>
        </AppBar>
        <Menu />
        <div>
          <AbsentRank />
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(Home);
