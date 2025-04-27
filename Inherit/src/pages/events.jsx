import styled from 'styled-components';

function events() {

  // 文化和旅游部关于公布2023—2025年国家级非物质文化遗产生产性保护示范基地名单的通知……

  // 长江文化艺术季系列活动之“国潮也疯狂·湖北非遗时装秀暨创新创意展”活动火热启幕……

  // 文化和旅游部关于公布第六批国家级非物质文化遗产代表性传承人的通知……


  return (
    <Container>
      <Title>文创产品</Title>
      <Title>视频教学</Title>
      <Title>定制服务</Title>
    </Container>
  )

}

export default events;

/***************************************************************
                        Styled Components
***************************************************************/
const Container = styled.div`
  display: flex;
  margin: 3em auto;
  max-width: 700px;
  border-radius: 8px;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: rgba(255, 255, 255, 0.5)
`

const Title = styled.h2`
  color:rgb(168, 68, 38);
  cursor: pointer;
  border-bottom: 1px solid rgb(168, 68, 38);
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