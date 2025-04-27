import styled from 'styled-components';
import { Outlet, useLocation } from 'react-router-dom';
import '@arco-design/web-react/dist/css/arco.css';
import background from './images/background.jpg'
import home from './images/home.jpg'
import AppBar from './components/AppBar';

function App () {
  const location = useLocation();
  const isHome = (location.pathname === '/home');
  return (
    <Container $isHome={isHome}>
      <AppBar />
      <Main>
        <Outlet />
      </Main>
    </Container>
  )
}

export default App;

/***************************************************************
                        Styled Components
***************************************************************/
const Container = styled.div`
  position: relative;
  min-height: 100vh;
  width: 100vw;
  background-position: top center;
  
  ${(props) => (props.$isHome ?
    `background-image: url(${home});
      background-size: cover;
    ` :
    `background-image: url(${background});
      background-size: initial;
    `
  )}
`;


const Main = styled.div`
  padding: 1em;
  overflow: auto;
`;