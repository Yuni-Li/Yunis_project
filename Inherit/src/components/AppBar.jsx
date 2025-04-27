import styled from 'styled-components';
import { useNavigate, useLocation } from 'react-router-dom';

function AppBar() {
  const navigate = useNavigate();
  const location = useLocation();

  // // 如果是welcomepage，隐藏导航栏
  // if (location.pathname === '/') return null;

  const routes = [
    { path: '/home', label: '首页' },
    { path: '/project', label: '非遗项目' },
    { path: '/user', label: '用户中心' },
    { path: '/relate', label: '相关资讯' },
    { path: '/events', label: '非遗活动' },
  ];

  // 高亮当前界面对应导航栏按键
  return (
    <Navbar>
      {routes.map(route => (
        <Button key={route.path}
          onClick={() => navigate(route.path)}
          $isActive={location.pathname === route.path}
        >
          {route.label}
        </Button>
      ))}
    </Navbar>
  )

}

export default AppBar;

/***************************************************************
                        Styled Components
***************************************************************/
const Navbar = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.5);
}
`;

const Button = styled.button`
  padding-top: 1vh;
  cursor: pointer;
  font-size: 1.1em;
  background-color: transparent;
  border: none;
  transition: all 0.3s ease;
  position: relative;
  color: ${(props) => (props.$isActive ? '	#2B6A94' : 'inherit')};
  transform: ${(props) => (props.$isActive ? 'scale(1.1)' : '1')};
  border-bottom: ${(props) => (props.$isActive ? '1px solid rgb(43, 106, 148)' : 'none')};
  
  &:hover {
    color:rgb(96, 167, 214);
    transform: scale(1.1);
    border-bottom: 1px solid rgb(43, 106, 148, 0.7);
  }

  &:active {
    transform: scale(0.98);
  }
`;