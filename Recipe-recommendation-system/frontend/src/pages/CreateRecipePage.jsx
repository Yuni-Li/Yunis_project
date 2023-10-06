import React from 'react';
import styled from 'styled-components';

// own components
import backgroundImage from '../image/2.jpg';
import CreateRecipeForm from '../components/CreateRecipeForm';

function CreateRecipePage() {
  return (
    <Wrapper>
      <Container>
        <CreateRecipeForm />
      </Container>
    </Wrapper>
  );
}

export default CreateRecipePage;

const Wrapper = styled.div`
  background-image: url(${backgroundImage});
  background-size: 100% 100%;
  height: 100vh;
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: auto;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.4);
  gap: 2rem;
`;
