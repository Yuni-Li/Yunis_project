import styled from 'styled-components';
import TitleImg from '../images/title.PNG'

function homePage() {


  return (
    <Container>
      <Title alt='Title'  src={TitleImg}/>
    </Container>
  )

}

export default homePage;

/***************************************************************
                        Styled Components
***************************************************************/
const Container = styled.div`
  width: 100%;
  text-align: center;
  padding: 6vw 0 6vw 0;
`;

const Title = styled.img`
  width: 60vw;
`