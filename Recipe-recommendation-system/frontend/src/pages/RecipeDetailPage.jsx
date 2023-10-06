import React from 'react';
import styled from 'styled-components';
import { useParams } from 'react-router-dom';

import backgroundImage from '../image/2.jpg';
import RecipeDetailForm from '../components/RecipeDetailForm';

function RecipeDetailPage() {
  const { recipeId } = useParams();

  return (
    <Wrapper>
      <Container>
        <RecipeDetailForm recipeId={recipeId} />
      </Container>
    </Wrapper>
  );
}

export default RecipeDetailPage;

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
