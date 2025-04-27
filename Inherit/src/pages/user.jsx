import React from 'react';
import { Button, Form, Input, Radio, Checkbox, message } from 'antd';
import styled from 'styled-components';

function User() {
  const [messageApi, contextHolder] = message.useMessage();
  const [form] = Form.useForm(); 
  const style = {
    display: 'flex',
    flexDirection: 'column',
    gap: 8,
  };

  const success = () => {
    messageApi.open({
      type: 'success',
      content: '提交成功！',
    });
    form.resetFields();
  }

  return (
    <Container>
      <StyledForm
        form={form}
        layout='vertical'
      >
        <Form.Item 
          label="1. 年龄段" 
          name="age"
          rules={[{ required: true, message: '请选择年龄段' }]}
          >
          <Radio.Group style={style}>
            <Radio value="under18">18岁以下</Radio>
            <Radio value="18-25">18-25岁</Radio>
            <Radio value="26-35">26-35岁</Radio>
            <Radio value="36-45">36-45岁</Radio>
            <Radio value="46-55">46-55岁</Radio>
            <Radio value="56plus">56岁及以上</Radio>
          </Radio.Group>
        </Form.Item>
        <Form.Item 
          label="2. 职业" 
          name="work"
          rules={[{ required: true, message: '请选择职业' }]}
          >
          <Radio.Group style={style}>
            <Radio value="student">学生</Radio>
            <Radio value="artist">教师/教育工作者</Radio>
            <Radio value="worker">文化/艺术从业者</Radio>
            <Radio value="freework">自由职业者</Radio>
            <Radio value="ohters">其他（请填写）</Radio>
            <Input placeholder="请填写其他职业" />
          </Radio.Group>
        </Form.Item>
        <Form.Item 
          label="3. 对荆州非遗文化的了解程度如何"
          name="know"
          rules={[{ required: true, message: '请选择了解程度' }]}
          >
          <Radio.Group style={style}>
            <Radio value="very">非常熟悉（能列举具体项目）</Radio>
            <Radio value="soso">一般了解（知道部分项目）</Radio>
            <Radio value="little">仅听说过名称</Radio>
            <Radio value="none">完全不了解</Radio>
          </Radio.Group>
        </Form.Item>
        <Form.Item label="4. 注册目的（可多选）" name="purposes">
          <Checkbox.Group style={style}>
            <Checkbox value="learn">学习非遗知识</Checkbox>
            <Checkbox value="activities">参与非遗活动</Checkbox>
            <Checkbox value="communication">与其他爱好者交流</Checkbox>
            <Checkbox value="support">支持非遗传承</Checkbox>
            <Checkbox value="other">其他（请填写））</Checkbox>
            <Input placeholder="请填写其他目的" />
          </Checkbox.Group>
        </Form.Item>
        <Form.Item label="5. 感兴趣的文化类别（可多选）" name="class">
          <Checkbox.Group style={style}>
            <Checkbox value="music">传统音乐（如马山民歌、啰啰咚）</Checkbox>
            <Checkbox value="the">传统戏剧（如荆河戏）</Checkbox>
            <Checkbox value="thea">曲艺（如鼓盆歌、说鼓子）</Checkbox>
            <Checkbox value="hand">手工技艺（如铅锡刻锈、漆器髹饰）</Checkbox>
            <Checkbox value="fest">民俗节庆</Checkbox>
            <Checkbox value="other">其他（请填写）</Checkbox>
            <Input placeholder="请填写其他目的" />
          </Checkbox.Group>
        </Form.Item>
        <Form.Item label="6. 希望在平台上看到的内容和功能（可多选）" name="hope">
          <Checkbox.Group style={style}>
            <Checkbox value="pic">非遗项目图文/视频介绍</Checkbox>
            <Checkbox value="live">线上直播教学（如技艺演示）</Checkbox>
            <Checkbox value="event">线下活动预约（如展览、体验课）</Checkbox>
            <Checkbox value="master">非遗传承人访谈</Checkbox>
            <Checkbox value="commu">互动社区（论坛、讨论区）</Checkbox>
            <Checkbox value="shop">非遗周边商城</Checkbox>
            <Checkbox value="other">其他（请填写）</Checkbox>
            <Input placeholder="请填写其他目的" />
          </Checkbox.Group>
        </Form.Item>
        <Form.Item label="7. 是否愿意接受我们的推荐内容和活动" name="notif">
          <Radio.Group style={style}>
            <Radio value="yes">愿意（通过站内消息/邮件/短信通知）</Radio>
            <Radio value="or">仅愿意接受站内消息推荐</Radio>
            <Radio value="no">暂不需要</Radio>
          </Radio.Group>
        </Form.Item>
        <Form.Item label="8. 对荆州非遗文化交流互动平台的期待和建议（选填）" name="advise">
          <Input/>
        </Form.Item>
        {contextHolder}
        <StyledButton type='primary' onClick={success}>提交</StyledButton>
      </StyledForm>
    </Container>

  )
};

export default User;

/***************************************************************
                        Styled Components
***************************************************************/
const Container = styled.div`
  display: flex;
  max-width: 100vw;
  justify-content: center;
  padding: 2em;
  overflow: hidden;

`;

const StyledForm = styled(Form)`
  padding: 2em;
  width: 100%;
  max-width: 750px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  overflow: hidden;
`;

const StyledButton = styled(Button)`
  align-items: center;
`;