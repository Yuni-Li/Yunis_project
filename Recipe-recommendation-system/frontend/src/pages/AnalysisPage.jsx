import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';

// MUI Component
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import Tabs from '@mui/material/Tabs';
import TabPanel from '@mui/lab/TabPanel';
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

ChartJS.register(...registerables);

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
    fontWeight: 'bold',
    fontSize: 20,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 15,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

function AnalysisPage() {
  const token = localStorage.getItem('token');
  const myUserID = localStorage.getItem('user_id');
  // console.log(token);
  // console.log(myUserID);
  const [dataForIngredients, setDataForIngredients] = React.useState([]);
  const [dataForRecipes, setDataForRecipes] = React.useState([]);
  const [dataForUsers, setDataForUsers] = React.useState([]);
  const [value, setValue] = React.useState('1');

  const backgroundColors = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)',
  ];
  const borderColors = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
  ];

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const getSetofIngredients = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch(`http://127.0.0.1:5000/analysis/ingredients?user_id=${myUserID}&token=${token}`, init)
      .then(res => res.json())
      .then(res => {
        console.log(res)
        if (res.top_ten_ingredients) {
          setDataForIngredients(res.top_ten_ingredients.map(function(item) {
            const data = {}
            data.name = item.ingredients_set;
            data.count = item.count;
            return data;
          }))
        }
      })
  }

  const getTopRecipes = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch(`http://127.0.0.1:5000/analysis/recipes?user_id=${myUserID}&token=${token}`, init)
      .then(res => res.json())
      .then(res => {
        if (res.top_five_recipes) {
          setDataForRecipes(res.top_five_recipes.map(function(item) {
            const data = {}
            data.recipe_id = item.recipe_id
            data.recipe_name = item.recipe_name;
            data.collections = item.collections;
            return data;
          }))
        }
      })
  }

  const getTopUsers = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch(`http://127.0.0.1:5000/analysis/users?user_id=${myUserID}&token=${token}`, init)
      .then(res => res.json())
      .then(res => {
        if (res.top_five_users) {
          setDataForUsers(res.top_five_users.map(function(item) {
            const data = {}
            data.email = item.email;
            data.user_id = item.user_id;
            data.username = item.username;
            data.followers = item.followers;
            return data;
          }))
        }
      })
  }

  React.useEffect(() => {
    getSetofIngredients();
    getTopRecipes();
    getTopUsers();
  }, [])

  // console.log(dataForIngredients)
  return (
    <Wrapper>
      <Container>
        <Box sx={{ width: '100%', typography: 'body1' }}>
          <TabContext value={value}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider', background: 'rgba(215, 0, 15, 0.6)' }}>
              <Tabs
                value={value}
                onChange={handleChange}
                variant="fullWidth"
              >
                <Tab value="1" label="Top 10 most frequently searched set of ingredients with no results" sx={{ color: '#ffffff', fontWeight: 'bold', fontSize: '15pt' }} />
                <Tab value="2" label="Top 5 most bookmarked recipes" sx={{ color: '#ffffff', fontWeight: 'bold', fontSize: '15pt' }} />
                <Tab value="3" label="Top 5 contributors with the most followers" sx={{ color: '#ffffff', fontWeight: 'bold', fontSize: '15pt' }} />
              </Tabs>
            </Box>
            <TabPanel value="1" sx={{ height: '77.1vh', overflow: 'auto' }} >
              <br />
              <br />
              <TableContainer component={Paper} sx={{ boxShadow: 'rgba(0, 0, 0, 0.50) 2px 2px 2px 2px' }}>
                <Table sx={{ width: '100%' }} >
                  <TableHead>
                    <TableRow>
                      <StyledTableCell sx={{ width: '80%' }}>Set of Ingredients</StyledTableCell>
                      <StyledTableCell align="right" sx={{ width: '20%' }}>Times of searches</StyledTableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {dataForIngredients.map((data) => (
                      <StyledTableRow
                        key={data.name}
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                      >
                        <StyledTableCell component="th" scope="row" sx={{ width: '80%' }}>
                          {data.name.join(', ')}
                        </StyledTableCell>
                        <StyledTableCell align="right" sx={{ width: '20%' }}>{data.count}</StyledTableCell>
                      </StyledTableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value="2" sx={{ height: '77.1vh', width: '120vh', overflow: 'auto' }} style={{ margin: 'auto' }}>
              <br />
              <br />
              <Bar
                data={{
                  labels: dataForRecipes.map(recipe => recipe.recipe_name),
                  datasets: [{
                    data: dataForRecipes.map(recipe => recipe.collections),
                    label: 'Number of collections',
                    backgroundColor: backgroundColors[0],
                    borderColor: borderColors[0],
                    borderWidth: 1,
                  }]
                }}
                options={{
                  onClick: function(e, element) {
                    if (element.length > 0) {
                      console.log(element[0].index)
                      window.open(`recipe/${dataForRecipes[element[0].index].recipe_id}`);
                    }
                  }
                }}
              />
            </TabPanel>
            <TabPanel value="3" sx={{ height: '77.1vh', width: '70vh', overflow: 'auto' }} style={{ margin: 'auto' }} >
              <br />
              <br />
              <Pie
                data={{
                  labels: dataForUsers.map(user => user.username),
                  datasets: [{
                    data: dataForUsers.map(user => user.followers),
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1,
                  }]
                }}
                options={{
                  onClick: function(e, element) {
                    if (element.length > 0) {
                      const index = element[0].index;
                      const userId = dataForUsers[index].user_id;
                      const email = dataForUsers[index].email;
                      if (myUserID === userId) {
                        window.open(`profile/${email}`);
                      } else {
                        window.open(`personal-detail/${userId}`);
                      }
                    }
                  }
                }}
              />
            </TabPanel>
          </TabContext>
        </Box>
      </Container>
    </Wrapper>
  );
}
export default AnalysisPage;

const Wrapper = styled('div')({
  height: '100vh',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  background: 'rgba(240, 194, 162, 0.7)',
});

const Container = styled('div')({
  position: 'fixed',
  top: '5vh',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: '1rem',
  background: 'rgba(255, 255, 255, 1)',
  boxShadow: 'rgba(0, 0, 0, 0.50) 1.95px 1.95px 2.6px',
  margin: 'auto',
  width: '90vw',
  height: '90vh',
  borderRadius: '10px',
  overflow: 'auto',
});
