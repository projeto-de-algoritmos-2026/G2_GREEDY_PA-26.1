import { FormEvent, useEffect, useMemo, useState } from 'react';
import {
  type Task,
  type ScheduledTask,
  type Priority,
  fetchTasks,
  createTask as apiCreateTask,
  updateTask as apiUpdateTask,
  deleteTask as apiDeleteTask,
  fetchWorkweekSchedule,
} from './api';

type TaskFormState = {
  name: string;
  duration: string;
  deadline: string;
  priority: Priority;
};

type CalendarDay = {
  date: Date;
  tasks: ScheduledTask[];
};

const priorityLabels: Record<Priority, string> = {
  tranquila: 'Tranquila',
  normal: 'Normal',
  importante: 'Importante',
};

const priorityClassName: Record<Priority, string> = {
  tranquila: 'priority-tag priority-tranquila',
  normal: 'priority-tag priority-normal',
  importante: 'priority-tag priority-importante',
};

function formatDeadline(deadline: string) {
  if (!deadline) {
    return 'Sem prazo';
  }

  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(deadline));
}

function formatMinutes(minutes: number) {
  return `${minutes} min`;
}

function formatTimeRange(start: Date, end: Date) {
  const formatter = new Intl.DateTimeFormat('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  });

  return `${formatter.format(start)} - ${formatter.format(end)}`;
}

function formatWeekday(date: Date) {
  const weekday = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'short',
  }).format(date);

  return weekday.replace('.', '');
}

function formatDayNumber(date: Date) {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
  }).format(date);
}

function formatWeekRange(start: Date, end: Date) {
  return `${formatDayNumber(start)} - ${formatDayNumber(end)}`;
}

function startOfWeek(date: Date) {
  const normalized = new Date(date);
  normalized.setHours(0, 0, 0, 0);

  const currentDay = normalized.getDay();
  const diffToMonday = currentDay === 0 ? -6 : 1 - currentDay;
  normalized.setDate(normalized.getDate() + diffToMonday);

  return normalized;
}

function addDays(date: Date, amount: number) {
  const nextDate = new Date(date);
  nextDate.setDate(nextDate.getDate() + amount);
  return nextDate;
}

function isSameDay(firstDate: Date, secondDate: Date) {
  return (
    firstDate.getFullYear() === secondDate.getFullYear() &&
    firstDate.getMonth() === secondDate.getMonth() &&
    firstDate.getDate() === secondDate.getDate()
  );
}

function calculateTotalTime(tasks: Task[]) {
  return tasks.reduce((total, task) => total + task.duration, 0);
}

function buildWeeklyCalendar(tasks: ScheduledTask[], weekOffset: number) {
  const currentWeekStart = startOfWeek(new Date());
  const selectedWeekStart = addDays(currentWeekStart, weekOffset * 7);

  const days: CalendarDay[] = Array.from({ length: 7 }, (_, index) => {
    const date = addDays(selectedWeekStart, index);

    return {
      date,
      tasks: tasks.filter((task) => isSameDay(task.suggestedStart, date)),
    };
  });

  return {
    weekStart: selectedWeekStart,
    weekEnd: addDays(selectedWeekStart, 6),
    days,
  };
}

const emptyFormState: TaskFormState = {
  name: '',
  duration: '',
  deadline: '',
  priority: 'normal',
};

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [orderedTasks, setOrderedTasks] = useState<ScheduledTask[]>([]);
  const [formState, setFormState] = useState<TaskFormState>(emptyFormState);
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [weekOffset, setWeekOffset] = useState(0);

  const totalTime = useMemo(() => calculateTotalTime(tasks), [tasks]);
  const weeklyCalendar = useMemo(
    () => buildWeeklyCalendar(orderedTasks, weekOffset),
    [orderedTasks, weekOffset],
  );

  async function refresh() {
    try {
      const updatedTasks = await fetchTasks();
      setTasks(updatedTasks);
      const schedule = await fetchWorkweekSchedule(updatedTasks);
      setOrderedTasks(schedule);
    } catch (err) {
      console.error('Erro ao atualizar dados:', err);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  function resetForm() {
    setFormState(emptyFormState);
    setEditingTaskId(null);
  }

  function startEditingTask(task: Task) {
    setEditingTaskId(task.id);
    setFormState({
      name: task.name,
      duration: String(task.duration),
      deadline: task.deadline,
      priority: task.priority,
    });
  }

  async function removeTask(taskId: string) {
    try {
      await apiDeleteTask(taskId);
      if (editingTaskId === taskId) resetForm();
      await refresh();
    } catch (err) {
      console.error('Erro ao remover tarefa:', err);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedName = formState.name.trim();
    const parsedDuration = Number(formState.duration);

    if (!trimmedName || Number.isNaN(parsedDuration) || parsedDuration <= 0) {
      return;
    }

    const taskPayload = {
      name: trimmedName,
      duration: parsedDuration,
      deadline: formState.deadline,
      priority: formState.priority,
    };

    try {
      if (editingTaskId) {
        await apiUpdateTask(editingTaskId, taskPayload);
      } else {
        await apiCreateTask(taskPayload);
      }
      resetForm();
      await refresh();
    } catch (err) {
      console.error('Erro ao salvar tarefa:', err);
    }
  }

  return (
    <div className="app-shell">
      <header className="hero-card">
        <div className="hero-meta">Planejamento semanal</div>
        <h1>Gerenciador de Tarefas</h1>
        <p>Organize estudos e entregas em uma ordem simples, com visão da semana.</p>

        <div className="hero-calendar">
          <div className="hero-calendar-top">
            <div>
              <span className="hero-calendar-label">Semana</span>
              <strong>{formatWeekRange(weeklyCalendar.weekStart, weeklyCalendar.weekEnd)}</strong>
            </div>
            <div className="hero-calendar-actions">
              <button
                className="button button-secondary"
                type="button"
                onClick={() => setWeekOffset((current) => current - 1)}
              >
                Semana anterior
              </button>
              <button
                className="button button-subtle"
                type="button"
                onClick={() => setWeekOffset(0)}
              >
                Semana atual
              </button>
              <button
                className="button button-secondary"
                type="button"
                onClick={() => setWeekOffset((current) => current + 1)}
              >
                Próxima semana
              </button>
            </div>
          </div>

          <div className="week-calendar-grid">
            {weeklyCalendar.days.map((day) => (
              <article className="week-day-column" key={day.date.toISOString()}>
                <div className="week-day-header">
                  <span>{formatWeekday(day.date)}</span>
                  <strong>{formatDayNumber(day.date)}</strong>
                </div>

                <div className="week-day-tasks">
                  {day.tasks.length > 0 ? (
                    day.tasks.map((task) => (
                      <div className="calendar-task" key={task.id}>
                        <div className="calendar-task-time">
                          {formatTimeRange(task.suggestedStart, task.suggestedEnd)}
                        </div>
                        <strong>{task.name}</strong>
                        <div className="calendar-task-tags">
                          <span className="info-pill">{formatMinutes(task.duration)}</span>
                          <span className={priorityClassName[task.priority]}>
                            {priorityLabels[task.priority]}
                          </span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="week-day-empty">Sem tarefas planejadas</div>
                  )}
                </div>
              </article>
            ))}
          </div>
        </div>
      </header>

      <main className="layout-grid">
        <section className="card form-card">
          <div className="section-heading">
            <div>
              <span className="section-kicker">Cadastro</span>
              <h2>{editingTaskId ? 'Editar tarefa' : 'Nova tarefa'}</h2>
            </div>
            <div className="section-summary">
              <span>{tasks.length} tarefas</span>
              <span>{formatMinutes(totalTime)}</span>
            </div>
          </div>

          <form className="task-form" onSubmit={handleSubmit}>
            <label className="field">
              <span>O que você precisa fazer?</span>
              <input
                type="text"
                placeholder="Ex.: Resolver exercícios da disciplina"
                value={formState.name}
                onChange={(event) =>
                  setFormState((current) => ({ ...current, name: event.target.value }))
                }
                required
              />
            </label>

            <div className="field-row">
              <label className="field">
                <span>Quanto tempo leva?</span>
                <input
                  type="number"
                  min="1"
                  placeholder="60"
                  value={formState.duration}
                  onChange={(event) =>
                    setFormState((current) => ({ ...current, duration: event.target.value }))
                  }
                  required
                />
              </label>

              <label className="field">
                <span>É muito importante?</span>
                <select
                  value={formState.priority}
                  onChange={(event) =>
                    setFormState((current) => ({
                      ...current,
                      priority: event.target.value as Priority,
                    }))
                  }
                >
                  <option value="tranquila">Tranquila</option>
                  <option value="normal">Normal</option>
                  <option value="importante">Importante</option>
                </select>
              </label>
            </div>

            <label className="field">
              <span>Tem horário para terminar?</span>
              <input
                type="datetime-local"
                value={formState.deadline}
                onChange={(event) =>
                  setFormState((current) => ({ ...current, deadline: event.target.value }))
                }
              />
            </label>

            <div className="form-actions">
              <button className="button button-primary" type="submit">
                {editingTaskId ? 'Salvar tarefa' : 'Adicionar tarefa'}
              </button>

              {editingTaskId && (
                <button className="button button-secondary" type="button" onClick={resetForm}>
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </section>

        <section className="card list-card">
          <div className="section-heading">
            <div>
              <span className="section-kicker">Tarefas</span>
              <h2>Minhas tarefas</h2>
            </div>
          </div>

          <div className="task-list">
            {tasks.length === 0 && (
              <div className="empty-state">
                <strong>Nenhuma tarefa adicionada.</strong>
                <p>Use o formulário acima para começar a organizar sua semana.</p>
              </div>
            )}

            {tasks.map((task) => (
              <article className="task-card" key={task.id}>
                <div className="task-card-top">
                  <h3>{task.name}</h3>
                  <span className={priorityClassName[task.priority]}>
                    {priorityLabels[task.priority]}
                  </span>
                </div>

                <div className="task-info">
                  <span className="info-pill">{formatMinutes(task.duration)}</span>
                  <span className="info-pill">{formatDeadline(task.deadline)}</span>
                </div>

                <div className="task-actions">
                  <button
                    className="button button-subtle"
                    type="button"
                    onClick={() => startEditingTask(task)}
                  >
                    Editar
                  </button>
                  <button
                    className="button button-danger"
                    type="button"
                    onClick={() => removeTask(task.id)}
                  >
                    Apagar
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="card order-card">
          <div className="section-heading">
            <div>
              <span className="section-kicker">Sugestão</span>
              <h2>Ordem para fazer</h2>
            </div>
          </div>

          <div className="order-list">
            {orderedTasks.length === 0 && (
              <div className="empty-state">
                <strong>A ordem sugerida vai aparecer aqui.</strong>
                <p>Tarefas com prazo definido aparecem primeiro.</p>
              </div>
            )}

            {orderedTasks.map((task) => (
              <article className="order-card-item" key={task.id}>
                <div className="order-number">{task.position}</div>

                <div className="order-content">
                  <h3>{task.name}</h3>
                  <div className="task-info">
                    <span className="info-pill">{formatMinutes(task.duration)}</span>
                    <span className="info-pill">{formatDeadline(task.deadline)}</span>
                    <span className={priorityClassName[task.priority]}>
                      {priorityLabels[task.priority]}
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
