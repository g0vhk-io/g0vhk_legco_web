import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import Tabs, { Tab } from 'material-ui/Tabs';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Card, { CardActions, CardContent, CardMedia } from 'material-ui/Card';
import Button from 'material-ui/Button';
import Typography from 'material-ui/Typography';
import "isomorphic-fetch";

const styles = () => ({
  container: {
  },
  column: {
    position: 'relative',
    bottom: '0',
    float: 'left',
    width: '50%',
    height: '100%'
  },
  chat: {
    width: '80%',
    height: '50vh',
    border: '0'
  },
  card: {
    maxWidth: '50em',
    float: 'left',
    marginLeft: '0.5em',
  },
  media: {
    height: '20vh'
  }
});

class Panels extends Component {
  constructor(props) {
    super(props);
    this.state = { value: 0};
  }

  componentWillMount() {
    fetch('https://api.g0vhk.io/gov/consultation/').then(res => {
      res.json().then(data => {
        this.setState({... this.state ,consultation: data});
      });
    });
    fetch('https://api.g0vhk.io/news/').then(res => {
      res.json().then(data => {
        this.setState({... this.state , news:data});
      });
    });

  }

  handleChange(event, value)  {
    this.setState({...this.state, value: value });
  };

  renderConsultation() {
    const { classes } = this.props;
    const { consultation } = this.state;
    return (
        <div>
          <h2>現正刊登的諮詢文件</h2> 
          <Table>
            <TableHead>
               <TableRow>
                 <TableCell>諮詢文件</TableCell><TableCell>截止日期</TableCell>
               </TableRow>
            </TableHead>
            <TableBody>
            { consultation && 
              consultation.results.map( r => {
                return (
                  <TableRow key={r.key}>
                    <TableCell>
                      <a href={r.link}>
                        {r.title}
                      </a>
                    </TableCell>
                    <TableCell>
                      {r.date}
                    </TableCell>
                  </TableRow>);
              })
            }
            </TableBody>
          </Table>
        </div>
    );
  }

  renderNews() {
    const { classes } = this.props;
    return (
      <div>
        <h2>聊天室</h2>
        <iframe src="https://gitter.im/g0vhk-io/Lobby/~embed" className={classes.chat}/>
      </div>
    ); 
  }

  renderProjects() {
    const { classes } = this.props;
    return (
      <div>
        <br/>
        <Card className={classes.card}>
          <CardMedia
            className={classes.media}
            image="/static/data.png"
            title="民間開放數據庫"
          />
          <CardContent>
            <Typography variant="headline" component="h2">
              民間開放數據庫
            </Typography>
          </CardContent>
          <CardActions>
            <Button
              href="https://budgetq.g0vhk.io"
              target="_blank"
              size="small"
              color="primary"
            >
              前往             
            </Button>
          </CardActions>
        </Card>
        <Card className={classes.card}>
          <CardMedia
            className={classes.media}
            image="/static/budgetq.png"
            title="開支預算問題書面答覆搜尋器"
          />
          <CardContent>
            <Typography variant="headline" component="h2">
              開支預算問題書面答覆搜尋器  
            </Typography>
          </CardContent>
          <CardActions>
            <Button
              href="http://data.g0vhk.io"
              target="_blank"
              size="small"
              color="primary"
            >
              前往             
            </Button>
          </CardActions>
        </Card>

      </div>
    );
  }

  renderMain() {
    const { classes } = this.props;
    const { news } = this.state;
    return (
       <div className={classes.container}>
        <div>
          <h2>最新消息</h2>
          <Table>
            <TableBody>
            { news && 
              news.results.map( r => {
                return (<TableRow key={r.id}><TableCell><div dangerouslySetInnerHTML={{__html:r.text_ch}}></div></TableCell></TableRow>);
              })
            }
            </TableBody>
          </Table>

        </div>
       </div>
    );
  }

  render() {
    const { state } = this;
    const show = state.value == 0
    return (
      <div>
        <AppBar position="static">
          <Tabs value={ state.value} onChange={this.handleChange.bind(this)}>
            <Tab label="最新消息"/>
            <Tab label="聊天室"/>
            <Tab label="諮詢文件"/>
            <Tab label="其他項目"/>
          </Tabs>
        </AppBar>
        { state.value == 1  && this.renderNews()}
        { state.value == 0  && this.renderMain()}
        { state.value == 2  && this.renderConsultation()}
        { state.value == 3  && this.renderProjects()}
      </div> 

    );
  }
};

export default withStyles(styles)(Panels);
