import styled, { css } from 'styled-components';
import { useRef, useState } from "react";

import bg1 from '../images/鼓盆歌.jpeg'
import bg2 from '../images/说鼓子.jpeg'
import bg3 from '../images/民歌.jpeg'
import bg4 from '../images/啰啰.jpeg'
import bg5 from '../images/荆河戏.jpeg'
import bg6 from '../images/铅锡.jpeg'
import bg7 from '../images/漆器.jpeg'


function Project() {
  const [activeIndex, setActiveIndex] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const itemRefs = useRef([]);
  const containerRef = useRef(null);

  const items = [
    { 
      name: "鼓盆歌", 
      bgImage: bg1,
      inheritor: "李金楚 望熙诰",
      description: {
        history:[
          "鼓盆歌是一种古老的曲艺形式，可远溯到三千多年前的《诗经》与《周易》中“鼓缶、击缶”的记载，那时的鼓盆歌主要以娱乐为主。",
          "战国时期楚人把这种音乐形式发展为“瓴缶之乐”，成为与“钟鼓之乐”、“竽瑟之乐”相并列的三种音乐形态之一。庄子妻死，鼓盆而歌，体现了对生命轮回的超然与豁达。而这种以“鼓盆、击缶”讴歌生命的方式，至今仍流传在湖北省荆州地区，其原生态的表演形式：一面鼓，一对槌；焚香点灯， 数人围坐。风格遒劲，堪称荆楚文化的“活化石”，具有见证中华民族传统文化的独特价值。"
        ],
        features: [
          "表演形式：单人或双人击鼓（盆鼓或堂鼓）说唱，节奏自由，唱腔高亢悲凉。",
          "内容题材：传统曲目多含忠孝节义，现代新增红色故事、时事宣传等。",
          "文化价值：保留了楚地巫歌遗韵，是研究荆楚民俗与口头文学的重要载体。"
        ],
        repertoire: [
          "《绣荷包》",
          "《观花》",
          "《白蛇传》"
        ],
        preservation: [
          "2006年，沙市鼓盆歌列入湖北省首批非遗名录；2011年升格为国家级非遗（项目编号Ⅴ-110）。",
          "荆州市出台《非物质文化遗产保护条例》，设立专项基金，支持鼓盆歌的调研、记录和传习活动。"
        ]
      }
    },
    { 
      name: "说鼓子", 
      bgImage: bg2,
      inheritor: "沈兴亚",
      description: {
        history:[
          "说鼓子湖北曲种，又名“荆州说鼓”。流行于湖北荆州地区的石首、松滋、公安、监利等县，与石首邻近的湖南几个县也有流传。",
          "传说鼓子源于戏曲音乐，形成于清同治年间。早期艺人都是戏班中文、武场面的伴奏者，在不能演出时，往往三五相聚，靠清唱来卖艺。后来逐渐改为单独演唱，一人掌握唢呐、鼓、单钹、醒木 4件乐器，多在春节和秋收以后应农民邀请演唱。以后又出现了一些流浪艺人沿门说唱，减掉了单钹和醒木。舞台上演出的说鼓子，除独脚班外，还有2人或3人的表演形式，上手打鼓说唱，下手吹唢呐伴奏，并进行插白或答词。"
        ],
        features: [
          "演员端坐表演，自击书鼓（直径约20cm的小扁鼓）掌握节奏。",
          "传统演出配备简板或醒木，现代演出常加入二胡、三弦伴奏。",
          "“说白”（散白）与“唱腔”（韵文）交替进行。",
          "典型结构：开场诗→说白→唱段→说白过渡→结尾收腔。"
        ],
        repertoire: [
          "《大战洪洲》",
          "《柳荫奇缘》",
          "《孔雀东南飞》",
          "《清风亭》",
          "《望子成龙》"
        ],
        preservation: [
          "2008年列入湖北省级非遗名录",
          "2019年11月，说鼓子入选国家级非物质文化遗产代表性项目保护单位名单"
        ]
      }
    },
    { 
      name: "马山民歌", 
      bgImage: bg3,
      inheritor: "王兆珍",
      description: {
        history:[
          "马山民歌是湖北省荆州市荆州区马山镇及周边地区流传的古老民歌形式，其历史可追溯至春秋战国时期，深受楚文化影响，并在长期农耕生活中发展成熟。",
          "先秦至唐宋时期，马山民歌的源头与《楚辞》中的民间歌谣一脉相承，如《九歌》《离骚》中的祭祀歌、劳动号子等；汉代乐府诗《江南可采莲》等作品与马山民歌的即兴对唱风格相似，说明其历史悠久。",
          "明清时期，是马山民歌的成熟定型时期，江汉平原农耕文化兴盛，马山民歌与当地劳动生活（插秧、采茶、薅草等）紧密结合，形成独特的田歌体系，受荆州说唱艺术（如鼓盆歌、三棒鼓）影响，部分曲目融入叙事性内容。",
          "近现代，20世纪50年代，音乐工作者（如湖北民歌采集小组）对马山民歌进行系统整理，使其登上专业舞台。",
          "2008年，马山民歌被列入国家级非物质文化遗产名录（编号Ⅱ-102）。"
        ],
        features: [
          "音乐风格：其调式以五声音阶（宫、商、角、徵、羽）为主，旋律优美，节奏自由。唱腔高亢嘹亮，真假声结合，具有鲜明的荆楚山地特色。早期无乐器伴奏，后加入锣鼓、二胡等，但仍以清唱为主。",
          "表演形式：独唱，如《薅黄瓜》《喇叭调》等，多用于田间劳动时自娱自乐；对唱，男女即兴对答，如《猜调》《十绣》等，充满生活情趣；一领众和，劳动号子类曲目，如《打硪歌》，由一人领唱，众人应和。",
          "歌词内容：题材广泛，包括劳动生产（插秧、采茶）、爱情婚恋（《十想郎》）、民俗节庆（《闹元宵》）等。语言生动，多用比兴、叠词、方言俚语，如“姐儿门前一棵槐”（《槐花几时开》）。"
        ],
        repertoire: [
          "“喇叭调”：《翻一个对牡丹》",
          "“伙计调”：《我说老板是条牛》",
          "“叮当调”：《一收衣裳二看郎》",
          "“嘚嘚调”：《今年丰收有指望》",
          "“蛤蟆调”：《一个蛤蟆一张嘴》"
        ],
        preservation: [
          "2008年，马山民歌被列入国家级非物质文化遗产名录，获得专项保护资金。",
          "政府为代表性传承人提供津贴，鼓励其开展授徒、演出活动。",
          "对老艺人演唱进行高清录音、录像，建立完整的马山民歌数据库。",
          "整理出版《荆州马山民歌全集》，收录经典曲目、唱腔及历史背景。"
        ]
      }
    },
    { 
      name: "啰啰咚", 
      bgImage: bg4,
      inheritor: "田维银 王斯彬",
      description: {
        history:[
          "“啰啰咚”是流行于湖北荆州江陵、监利等地的传统田歌，其雏形可追溯至古代农耕社会的劳动号子。",
          "楚文化基因：与《楚辞》中的“劳者歌其事”传统一脉相承，类似《越人歌》的即兴演唱形式。",
          "劳动功能：最初为水田劳作（插秧、薅草）时统一节奏、缓解疲劳的集体歌唱，以“啰”“咚”等衬词得名",
          "曲艺化定型（明清至民国），明代吸收荆州道教音乐中的“诵唱”技法，形成“一领众和”的演唱结构。出现固定衬词套路（如“啰啰咚呀嗬嘿”）。",
          "清代，发展出完整的“五句子”歌词结构（七言五句为一章）。与马山民歌相互影响，形成“高腔啰啰咚”（音调高亢）和“平腔啰啰咚”（叙事性强）两种流派。",
          "民国时期，职业“歌师傅”出现，在红白喜事中表演，曲目扩展至《十二月采花》《十月怀胎》等。1936年《江陵县志》首次记载：“农人薅草，击鼓而歌，谓之啰啰咚”。"
        ],
        features: [
          "典型“一领众和”形式：领唱者（歌师傅）唱主词，众人（通常8-12人）应和衬词。",
          "多声部自然和声：形成纯四度、大二度等民间特色音程。",
          "自由散板与规整节奏交替。",
          "核心节奏型：X X X ｜ X — ｜（对应“啰啰 咚 呀”）"
        ],
        repertoire: [
          "《花“啰啰咚”》",
          "《也“啰啰咚”》",
          "《五色绒线绣一支花》"
        ],
        preservation: [
          "2007年列入湖北省非物质文化遗产名录",
          "2019年11月，《国家级非物质文化遗产代表性项目保护单位名单》公布，监利县文化馆获得啰啰咚项目保护单位资格。"
        ]
      }
    },
    { 
      name: "荆河戏", 
      bgImage: bg5,
      inheritor: "刘厚云",
      description: {
        history:[
          "2019年11月，《国家级非物质文化遗产代表性项目保护单位名单》公布，监利县文化馆获得啰啰咚项目保护单位资格。"
        ],
        features: [
          "荆州荆河戏作为湖北特色剧种，形成于明清时期，融合了弋阳腔、昆曲和汉调皮黄等声腔艺术，发展出以“西皮二黄”为主体、“五大声腔”并存的独特音乐体系。其艺术特点鲜明：表演上保留高腔“一唱众和”的古朴形式，拥有十大行当和“髯口功”“翎子功”等绝活；音乐上构建“九腔十八板”的完整板式，独创“滚板”“哭头”等演唱技法；舞台呈现则坚持明代服饰规制和五行脸谱系统，尤以“水纹脸”“鱼鳞甲”等荆州元素著称。"
        ],
        repertoire: [
          "《百子图》",
          "《楚宫抚琴》",
          "《大回荆州》",
          "《双驸马》"
        ],
        preservation: [
          "2006年列入湖北省首批非物质文化遗产名录",
          "2019年11月，《国家级非物质文化遗产代表性项目保护单位名单》公布，荆州市群众艺术馆（荆州市艺术研究所）、澧县荆河剧院演艺有限公司获得“荆河戏”项目保护单位资格。"
        ]
      }
    },
    { 
      name: "铅锡刻锈技艺", 
      bgImage: bg6,
      inheritor: "敖朝宗",
      description: {
        history:[
          "荆州铅锡刻镂技艺起源于商周青铜器铸造，经楚文化滋养形成独特风格，明清时期达到鼎盛，发展出“三层透雕”等精湛工艺。作为湖北省非物质文化遗产，该技艺完整保存了古代金属加工的“锻、錾、刻、镂”技术链，其分层叠加技法和楚式纹样具有重要文化价值。当代通过建立传习所、数字化保护等措施进行抢救性传承，并在文物修复领域创新应用，但面临人才培养周期长、机械化冲击等挑战，亟需在传统工艺保护与现代技术创新间寻求平衡发展。"
        ],
        features: [
          "分层透雕：独创“三层叠加”雕刻法，在铅锡合金上打造立体纹饰，展现繁复的楚式图案。",
          "古法工艺：完整传承锻打、錾刻、镂空等传统技法，严格把控铅锡配比，确保材质特性。",
          "文化传承：纹样保留楚风特色，工具自成一派，现代应用中仍坚守手工核心技艺。"
        ],
        repertoire: [
          "制模→雕刻→改动"
        ],
        preservation: [
          "2011年5月23日，铅锡刻镂技艺经中华人民共和国国务院批准列入第三批国家级非物质文化遗产名录，项目编号Ⅷ-194。",
          "创新应用：开发文创产品56款，年销售额破百万，其中“楚纹茶具”获2023年非遗设计金奖"
        ]
      }
    },
    { 
      name: "漆器髹技艺饰", 
      bgImage: bg7,
      inheritor: "邹德香",
      description: {
        history:[
          "荆州漆器髹饰技艺起源于战国楚文化时期，距今已有2500余年历史，以荆州楚墓出土的彩绘漆耳杯等文物为证，展现了早期成熟的夹纻胎工艺和独特的楚式凤鸟纹饰。历经汉唐发展，形成了针刻填金、堆漆造像等特色技法，至明清时期更创新出“荆州菠萝漆”等独门工艺。该技艺完整保存了18类传统髹饰技法，其矿物颜料制备体系尤为珍贵，2006年被列入湖北省非物质文化遗产名录。当代通过建立非遗工坊、数字复原古法配方等措施进行保护传承，并与国际漆艺界开展创新合作，但依然面临生漆过敏、技艺断层等传承挑战，亟待通过科技手段与传统工艺融合寻求突破发展。"
        ],
        features: [
          "独特胎艺：传承战国“夹纻胎”技法，创新“菠萝漆”肌理工艺",
          "髹饰绝活：建立矿物颜料体系，独创“针刻填金”装饰技法",
          "楚风纹饰：延续凤鸟云纹传统，发展“雕填”“堆漆”等装饰手法"
        ],
        repertoire: [
          "胎体制作→髹漆→彩绘"
        ],
        preservation: [
          "2006年被列入湖北省非物质文化遗产名录",
          "2019年11月，《国家级非物质文化遗产代表性项目保护单位名单》公布，荆州市群众艺术馆（荆州市艺术研究所）获得“漆器髹饰技艺（楚式漆器髹饰技艺）”项目保护单位资格"
        ]
      }
    },
  ]

  const handleItemClick = (index) => {
    setSelectedItem(selectedItem === index ? null : index)

    if (itemRefs.current[index]) {
      itemRefs.current[index].scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
        inline: 'center'
      });
    }
  }

  return (
    <Container ref={containerRef}>
      <HorizontalList>
        {items.map((item, index) => (
          <ListItems
            key={index}
            ref={el => itemRefs.current[index] = el}
            $bgImage={item.bgImage}
            $isActive={activeIndex === index}
            $isInActive={activeIndex !== null && activeIndex !== index}
            $isSelected={selectedItem === index}
            onMouseEnter={() => setActiveIndex(index)}
            onMouseLeave={() => setActiveIndex(null)}
            onClick={() => handleItemClick(index)}
          >
            <ItemContent>
              {item.name}
            </ItemContent>
          </ListItems>
        ))}

      </HorizontalList>

      {selectedItem !== null && (
        <DetailContainer>
          <DetailContent>
            <Inheritor>传承人： {items[selectedItem].inheritor}</Inheritor>

            <Section>
              <h3>历史沿革</h3>
              <div>{items[selectedItem].description.history.map(item => <p>{item}</p>)}</div>
            </Section>

            <Section>
              <h3>
              {["铅锡刻锈技艺", "漆器髹技艺饰"].includes(items[selectedItem].name) ? "工艺特征" : "艺术特点"}
              </h3>
              <ul>{items[selectedItem].description.features.map((fea, i) => <li key={i}>{fea}</li> )}</ul>
            </Section>

            <Section>
              <h3>
                {["铅锡刻锈技艺", "漆器髹技艺饰"].includes(items[selectedItem].name) ? "工艺流程" : "经典曲目"}
              </h3>
              <ul>
              {items[selectedItem].description.repertoire.map((rep, j) => (<li key={j}>{rep}</li>))}
              </ul>
            </Section>

            <Section>
              <h3>传承保护</h3>
              <ul>{items[selectedItem].description.preservation.map((pres, k) => <li key={k}>{pres}</li> )}</ul>
            </Section>
          </DetailContent>
        </DetailContainer>
      )}

    </Container>
  )
}

export default Project;

/***************************************************************
                        Styled Components
***************************************************************/
const Container = styled.div `
  overflow: auto;
  padding: 3vw 7vw;
`

const HorizontalList = styled.div `
  display: flex;
  height: 50vh;
`

const ListItems = styled.div `
  flex: 1;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  background-color: #fff;
  transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);

  background-image: url(${props => props.$bgImage});
  background-position: left;
  background-size: cover;
  background-repeat: no-repeat;


  ${({ $isSelected }) => $isSelected && css`
    flex: 3;
    border: 3px solid rgb(235, 235, 186);
    border-radius: 8px;
    box-shadow: 0 0 15px rgba(110, 15, 15, 0.7);
  `}

  ${({ $isSelected, $isActive }) =>
    !$isSelected && $isActive && css`
      flex: 1.5;
  `}

  ${({ $isSelected, $isInActive }) =>
    !$isSelected && $isInActive && css`
      flex: 0.5;
  `}
`

const ItemContent = styled.div `
  position: absolute;
  font-size: 1.5rem;
  color: white;
  top: 20px;
  writing-mode: vertical-rl;
`

const DetailContainer = styled.div`
  padding: 2em;
  background-color: rgba(255, 255, 255, 0.6);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
`

const DetailContent = styled.div`
  max-width: 1200px;
  margin: 0, auto;

  h2 {
    color: #000;
  }

  p {
    color: rgba(10, 10, 10);
    line-hight: 1.6;
  }
`

const Inheritor = styled.h2`
  text-align: right;
`

const Section = styled.section`
  margin-bottom: 2rem;
  
  h3 {
    color:rgb(159, 35, 35);
    border-bottom: 1px solid rgba(110, 15, 15, 0.7);
    padding-bottom: 0.5rem;
    margin-bottom: 0.8rem;
  }
  
  ul {
    padding-left: 1.2rem;
    
    li {
      margin-bottom: 0.5rem;
      line-height: 1.6;
    }
  }
`;