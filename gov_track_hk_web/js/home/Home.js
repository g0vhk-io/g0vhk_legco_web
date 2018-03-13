import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import Timer from './Timer';
import Facebook from './Facebook';
import { withStyles } from 'material-ui/styles';
import IconButton from 'material-ui/IconButton';
import TiSocialFacebook from 'react-icons/lib/ti/social-facebook';
import TiSocialGithub from 'react-icons/lib/ti/social-github';
import TiSocialTwitter from 'react-icons/lib/ti/social-twitter';
import Toolbar from 'material-ui/Toolbar';
import Panels from './Panels';
import TopBar from './Topbar';


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
  social: {
    float: 'left'
  }
});

class Home extends Component {
  render() {
    const { classes } = this.props;
    const socialButtons = (
      <div className={classes.social}>
        <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://www.facebook.com/g0vhk.io"
          >
            <IconButton>
              <TiSocialFacebook size={30} color="white" />
            </IconButton>
          </a>
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://github.com/g0vhk-io"
          >
            <IconButton>
              <TiSocialGithub size={30} color="white" />
            </IconButton>
          </a>
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://twitter.com/g0vhk_io"
          >
            <IconButton>
              <TiSocialTwitter size={30} color="white" />
            </IconButton>
          </a>
      </div>
    );
    return (
      <div className={classes.container}>
         <TopBar/>
         <AppBar position="static" className={classes.appBar}>
           <div className={classes.jumbotron}>
             <h1><div>g0vhk.io</div></h1>
             <h1>{socialButtons} <Facebook /></h1>
             <Timer />
           </div>
        </AppBar>
        <Panels/>
      </div>
    );
  }
};

export default withStyles(styles)(Home);
