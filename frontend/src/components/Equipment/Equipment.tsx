import styles from "./Equipment.module.scss";
import { Inventory } from "../../static/types/Inventory";
import { states } from '../../static/data/states';
import { Link } from 'react-router-dom';

export function Equipment({equipment}: {equipment: Inventory}) {
  return (
    <div className={styles.equipment}>
      <img src={`${import.meta.env.VITE_API_URL}/${equipment.image}`} alt="" className={styles.image} />
      <div className={styles.info}>
        <div className={styles.name}>
          {equipment.name}
        </div>
        <div className={styles.state} style={{color: states[equipment.state].color}}>
          Состояние: {states[equipment.state].text}
        </div>
        <div className={styles.amount}>Количество: {equipment.amount} шт.</div>
        <div className={styles.btns}>
          <Link to={`/get/${equipment._id}`} className={styles.btn}>Получить</Link>
          <Link to={`/repair/${equipment._id}`} className={styles.btn}>Ремонт</Link>
        </div>
      </div>
    </div>
  )
}
