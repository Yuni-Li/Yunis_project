import styled from 'styled-components';

function relate() {

  // 文化和旅游部关于公布2023—2025年国家级非物质文化遗产生产性保护示范基地名单的通知……

  // 长江文化艺术季系列活动之“国潮也疯狂·湖北非遗时装秀暨创新创意展”活动火热启幕……

  // 文化和旅游部关于公布第六批国家级非物质文化遗产代表性传承人的通知……


  return (
    <Container>
      <Title>政策法规</Title>
      <Content>文化和旅游部关于公布2023—2025年国家级非物质文化遗产生产性保护示范基地名单的通知</Content>
      <Title>媒体关注</Title>
      <Content>长江文化艺术季系列活动之“国潮也疯狂·湖北非遗时装秀暨创新创意展”活动火热启幕</Content>
      <Title>新闻动态</Title>
      <Content>文化和旅游部关于公布第六批国家级非物质文化遗产代表性传承人的通知</Content>
    </Container>
  )

}

export default relate;

/***************************************************************
                        Styled Components
***************************************************************/
const Container = styled.div`
  display: flex;
  margin: 2em auto;
  max-width: 800px;
  border-radius: 8px;
  padding-bottom: 5px;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: rgba(255, 255, 255, 0.5)
`

const Title = styled.h2`
  color:rgb(168, 68, 38);
  cursor: pointer;
  border-bottom: 1px solid rgb(147, 58, 31);
  transition: all 0.3s ease;

  &:hover {
    color:rgb(220, 92, 53);
    transform: scale(1.1);
    border-bottom: 1px solid rgb(220, 92, 53, 0.7);
  }

  &:active {
    transform: scale(0.98);
  }
`

const Content = styled.text`
  max-width: 85vw;
`